from flask import Flask, render_template
from orders.controllers.order_controller import order_controller
from db.db import db
from flask_cors import CORS
from flask_consulate import Consul

app = Flask(__name__)
CORS(app)

@app.route('/healthcheck')
def health_check():
    """
    This function is used to say current status to the Consul.
    Format: https://www.consul.io/docs/agent/checks.html

    :return: Empty response with status 200, 429 or 500
    """
    # TODO: implement any other checking logic.
    return 'OK', 200
app.config['CONSUL_HOST'] = 'consul-server'
app.config['CONSUL_PORT'] = 8500
# Consul
# This extension should be the first one if enabled:
consul = Consul(app=app)
# Fetch the conviguration:
consul.apply_remote_config(namespace='mynamespace/')
# Register Consul service:
consul.register_service(
    name='orders-microservice',
    interval='10s',
    tags=['microservice', 'orders' ],
    port=5004,
    httpcheck='http://orders:5004/healthcheck'
)

app.config.from_object('config.Config')
db.init_app(app)

# Registrando el blueprint del controlador de usuarios
app.register_blueprint(order_controller)

@app.after_request
def apply_cors_headers(response):
    response.headers['Access-Control-Allow-Origin'] = 'http://localhost:5001'
    response.headers['Access-Control-Allow-Credentials'] = 'true'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type,Authorization'
    response.headers['Access-Control-Allow-Methods'] = 'GET,POST,PUT,DELETE,OPTIONS'
    return response

if __name__ == '__main__':
    app.run()