import os
from app import create_app
from flask import Flask

if __name__ == '__main__':
    app = create_app(os.environ.get('FLASK_CONFIG', 'development'))
    app.run()
