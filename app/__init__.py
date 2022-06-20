import os
from flask import Flask

Transactions = []
PayerTotals = {}


def create_app(config_name):
    """
    Create an application instance. Load configuration and register blueprints
    
    """
    app = Flask(__name__)

    # apply configuration
    cfg = os.path.join(os.getcwd(), 'config', config_name + '.py')
    app.config.from_pyfile(cfg)

    # register blueprints
    from .api_v1 import api as api_blueprint
    app.register_blueprint(api_blueprint, url_prefix='/api/v1')

    return app
