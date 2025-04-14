import os
import sys
import subprocess
import logging
from flask import Flask
from config import DevelopmentConfig, ProductionConfig

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger()

def build_tailwind():
    try:
        print("Building Tailwind CSS...")
        subprocess.run(["npm", "run", "build"], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error during Tailwind build: {e}")
        exit(1)

def watch_tailwind():
    try:
        print("Watching for Tailwind changes...")
        subprocess.Popen(["npm", "run", "watch"], shell=True)
    except subprocess.CalledProcessError as e:
        print(f"Error starting watch mode: {e}")
        exit(1)

def create_app():
    app = Flask(__name__, template_folder=os.path.join(os.getcwd(), 'templates'), static_folder=os.path.join(os.getcwd(), 'static'))

    env = os.getenv('FLASK_ENV', 'development')
    if env == 'production':
        app.config.from_object(ProductionConfig)
        build_tailwind()
    elif env == 'development':
        app.config.from_object(DevelopmentConfig)
        watch_tailwind()
    else:
        logger.critical(f"ERROR: Environment '{env}' does not exist")
        sys.exit(1)

    logger.info(f"[Flask] Starting in '{env}' mode.")

    from .routes import main
    app.register_blueprint(main)

    return app