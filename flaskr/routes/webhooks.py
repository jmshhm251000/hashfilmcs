import logging
from flask import Blueprint, current_app, request, abort
from pythonjsonlogger import jsonlogger

# Set up a logger for this module with JSON formatting
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# Create a file handler that logs INFO messages
file_handler = logging.FileHandler("webhook.log")
file_handler.setLevel(logging.INFO)

# Create a JSON formatter; adjust fields as desired
formatter = jsonlogger.JsonFormatter('%(asctime)s %(name)s %(levelname)s %(message)s')
file_handler.setFormatter(formatter)

# Add the file handler to the logger
logger.addHandler(file_handler)

# Create a Blueprint for your webhook
webhook_bp = Blueprint('webhook', __name__)

@webhook_bp.route('/webhook', methods=['GET', 'POST'])
def webhook():
    VERIFY_TOKEN = current_app.config.get('VERIFY_TOKEN')

    if request.method == 'GET':
        mode = request.args.get('hub.mode')
        token = request.args.get('hub.verify_token')
        challenge = request.args.get('hub.challenge')
        
        # Log the GET request as a JSON message
        logger.info({
            "event": "GET webhook verification request",
            "mode": mode,
            "token": token,
            "challenge": challenge,
            "remote_addr": request.remote_addr,
            "url": request.url,
            "extra_field": request.args.get('field')
        })
        
        if mode == 'subscribe' and token == VERIFY_TOKEN:
            logger.info({"event": "Webhook verified successfully"})
            return challenge, 200
        else:
            logger.warning({
                "event": "Verification token mismatch",
                "mode": mode,
                "token": token,
                "remote_addr": request.remote_addr
            })
            return 'Verification token mismatch', 403

    elif request.method == 'POST':
        data = request.get_json()
        # Log POST request details in JSON format
        logger.info({
            "event": "POST webhook event received",
            "method": request.method,
            "url": request.url,
            "remote_addr": request.remote_addr,
            "headers": dict(request.headers),
            "data": data
        })
        return 'EVENT_RECEIVED', 200