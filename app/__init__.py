""" Module containing flask application """
import os
from flask import Flask

"""
Data structures containing transactions and points per payer
Transactions: [
    {
        payer: <payer name>
        points: <points added by transaction>
        points_remaining: <points not spent yet for this transaction>
        timestamp: <timestamp the transaction was made
    },
]
PayerTotals: {
    <payer name>: <totals points for payer>
}
"""
Transactions = []
PayerTotals = {}


def create_app(config_name):
    """
    Create an application instance. Load configuration and register blueprints
    arguments:
        config_name - Which configuration to load from the app. Either "development",
            "testing", or "production"
    returns: application instance

    """
    app = Flask(__name__)

    # apply configuration
    cfg = os.path.join(os.getcwd(), 'config', config_name + '.py')
    app.config.from_pyfile(cfg)

    # register blueprints
    from .api_v1 import api as api_blueprint
    app.register_blueprint(api_blueprint, url_prefix='/api/v1')

    return app
