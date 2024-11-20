import subprocess
from pyngrok import ngrok
import threading
import time


def run_app():
    subprocess.run(["python", "app.py"])


def run_ngrok():
    public_url = ngrok.connect(5000)
    print(f"ngrok tunnel available at: {public_url}")


if __name__ == "__main__":
    # Start the Flask app in a separate thread
    app_thread = threading.Thread(target=run_app)
    app_thread.start()

    # Give the Flask app some time to start
    time.sleep(5)

    # Start ngrok
    run_ngrok()

    # Keep the script running
    app_thread.join()
