import os
import sys
import subprocess
import logging
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import DevelopmentConfig, ProductionConfig
from flask_migrate import Migrate

import pymysql

pymysql.install_as_MySQLdb()

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger()

def build_tailwind():
    try:
        print("Building Tailwind CSS...")
        subprocess.run(["npm", "run", "build"], check=True)
    except subprocess.CalledProcessError as e:
        logger.error(f"Error during Tailwind build: {e}")
        exit(1)

def watch_tailwind():
    try:
        print("Watching for Tailwind changes...")
        subprocess.Popen(["npm", "run", "watch"])
    except subprocess.CalledProcessError as e:
        logger.error(f"Error starting watch mode: {e}")
        exit(1)

def check_db_connection(app):
    try:
        db = SQLAlchemy(app)
        with app.app_context():
            db.engine.connect()
        logger.info("Database connection successful!")
        return db
    except Exception as e:
        logger.critical(f"Database connection failed: {e}")
        sys.exit(1)

def create_app():
    app = Flask(__name__, template_folder=os.path.join(os.getcwd(), 'templates'),
                static_folder=os.path.join(os.getcwd(), 'static'))

    env = os.getenv('FLASK_ENV', 'development')

    if env == 'production':
        app.config.from_object(ProductionConfig)
        db = check_db_connection(app)
        build_tailwind()
    elif env == 'development':
        app.config.from_object(DevelopmentConfig)
        db = check_db_connection(app)
        watch_tailwind()
    else:
        logger.critical(f"ERROR: Environment '{env}' does not exist")
        sys.exit(1)

    migrate = Migrate(app, db)
    logger.info(f"[Flask] Starting in '{env}' mode.")

    from .routes import main
    app.register_blueprint(main)

    return app