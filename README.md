Robot Teleoperation System
This repository contains a web-based robot teleoperation system that allows users to control a robot remotely using a web interface. The system provides real-time video streaming from the robot's camera and joystick control for precise movements.

Features
Secure authenticated access to the control system
Real-time joystick control for precise robot movement
Live video feed from the robot's camera
Real-time feedback and status monitoring

Key Files
app.py: Main application file that initializes the Flask app, sets up routes, and handles camera configuration and frame processing.
models.py: Contains the database models for the application, including the User model for authentication.
requirements.txt: Lists the dependencies required for the project.
templates: Contains HTML templates for the web interface, including login, registration, control panel, and index pages.

Installation
1. Clone the repository:
git clone https://github.com/isaiperezhr/Inu-Robot.git
cd Inu-Robot

2. Install the required dependencies:
pip install -r requirements.txt

Usage
1. Run the application:
python3 server.py
2. Open in a web browser the URL provided by Ngrok.
3. Register a new user or log in with an existing account.
4. Access the control panel to view the live video feed and control the robot.

Configuration
- The application uses SQLite as the database. The database file is created in the instance directory.
- Camera settings such as resolution, frame rate, and JPEG quality can be configured in the CameraConfig class in app.py.

Dependencies:
- Flask
- Flask-Login
- Flask-SQLAlchemy
- Flask-SocketIO
- Werkzeug
- SQLAlchemy
- python-socketio
- python-engineio
- simple-websocket
- opencv-python
- numpy
- pyzmq
- pyngrok

License
This project is licensed under the MIT License. See the LICENSE file for details.

Contributing
Contributions are welcome! Please open an issue or submit a pull request for any improvements or bug fixes.