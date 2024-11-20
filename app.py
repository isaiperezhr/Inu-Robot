from flask import Flask, render_template, redirect, url_for, flash, request
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from flask_socketio import SocketIO
from models import db, User
import cv2
import logging
import base64
import threading
import time

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins='*', async_mode='threading')

# Configuration
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize extensions
db.init_app(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


class CameraConfig:
    def __init__(self, width=640, height=480):
        self.width = width
        self.height = height
        self.camera = None
        self.running = False
        self.target_fps = 30
        self.frame_interval = 1.0 / self.target_fps
        self.jpeg_quality = 70

    def initialize(self):
        try:
            logger.info("Initializing camera...")
            self.camera = cv2.VideoCapture(0)
            self.camera.set(cv2.CAP_PROP_FRAME_WIDTH, self.width)
            self.camera.set(cv2.CAP_PROP_FRAME_HEIGHT, self.height)
            self.camera.set(cv2.CAP_PROP_FPS, self.target_fps)
            self.camera.set(cv2.CAP_PROP_BUFFERSIZE, 1)

            if not self.camera.isOpened():
                logger.error("Failed to open camera")
                return False

            self.running = True
            return True
        except Exception as e:
            logger.error(f"Camera initialization error: {str(e)}")
            return False

    def cleanup(self):
        self.running = False
        if self.camera is not None:
            self.camera.release()


# Initialize camera configuration
camera_config = None


def process_frames():
    """Capture and emit frames via WebSocket."""
    last_frame_time = time.time()
    frame_count = 0

    while camera_config.running:
        current_time = time.time()
        if current_time - last_frame_time < camera_config.frame_interval:
            continue

        try:
            # Clear buffer by reading multiple frames
            for _ in range(2):
                camera_config.camera.grab()

            ret, frame = camera_config.camera.read()
            if ret:
                # Compress frame
                _, buffer = cv2.imencode(
                    '.jpg', frame,
                    [cv2.IMWRITE_JPEG_QUALITY, camera_config.jpeg_quality]
                )
                frame_data = base64.b64encode(buffer).decode('utf-8')
                socketio.emit('frame', {'data': frame_data})

                frame_count += 1
                if frame_count % camera_config.target_fps == 0:
                    actual_fps = camera_config.target_fps / \
                        (time.time() - last_frame_time)
                    logger.debug(f"Streaming at {actual_fps:.1f} FPS")
                    frame_count = 0

                last_frame_time = time.time()

        except Exception as e:
            logger.error(f"Frame processing error: {str(e)}")
            time.sleep(0.1)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Routes


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/control')
@login_required
def control():
    return render_template('control.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('control'))

    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.query.filter_by(username=username).first()

        if user and user.check_password(password):
            login_user(user)
            next_page = request.args.get('next')
            return redirect(next_page if next_page else url_for('control'))

        flash('Invalid username or password')
    return render_template('login.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('control'))

    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        if User.query.filter_by(username=username).first():
            flash('Username already exists')
            return redirect(url_for('register'))

        user = User(username=username)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('login'))

    return render_template('register.html')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))


def init_db():
    with app.app_context():
        db.create_all()


if __name__ == '__main__':
    init_db()

    # Initialize camera
    camera_config = CameraConfig()
    if camera_config.initialize():
        # Start frame processing in a separate thread
        thread = threading.Thread(target=process_frames)
        thread.daemon = True
        thread.start()

    try:
        socketio.run(app, host='0.0.0.0', port=5000,
                     allow_unsafe_werkzeug=True)
    finally:
        if camera_config:
            camera_config.cleanup()
