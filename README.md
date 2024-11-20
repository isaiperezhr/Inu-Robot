
### Key Files

- [`app.py`](app.py): Main application file that initializes the Flask app, sets up routes, and handles camera configuration and frame processing.
- [`models.py`](models.py): Contains the database models for the application, including the `User` model for authentication.
- [`requirements.txt`](requirements.txt): Lists the dependencies required for the project.
- [`templates`](templates): Contains HTML templates for the web interface, including login, registration, control panel, and index pages.

## Installation

1. Clone the repository:
    ```sh
    git clone https://github.com/yourusername/robot-teleoperation.git
    cd robot-teleoperation
    ```

2. Create and activate a virtual environment:
    ```sh
    python3 -m venv venv
    source venv/bin/activate
    ```

3. Install the required dependencies:
    ```sh
    pip install -r requirements.txt
    ```

4. Set up the database:
    ```sh
    python -c "from app import init_db; init_db()"
    ```

## Usage

1. Run the application:
    ```sh
    python app.py
    ```

2. Open a web browser and navigate to `http://localhost:5000`.

3. Register a new user or log in with an existing account.

4. Access the control panel to view the live video feed and control the robot.

## Configuration

- The application uses SQLite as the database. The database file is created in the `instance` directory.
- Camera settings such as resolution, frame rate, and JPEG quality can be configured in the `CameraConfig` class in `app.py`.

## Dependencies

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

## License

This project is licensed under the MIT License. See the LICENSE file for details.

## Acknowledgements

- [Flask](https://flask.palletsprojects.com/)
- [OpenCV](https://opencv.org/)
- [Socket.IO](https://socket.io/)

## Contributing

Contributions are welcome! Please open an issue or submit a pull request for any improvements or bug fixes.