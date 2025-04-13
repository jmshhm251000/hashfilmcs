import logging
from flask import Blueprint, current_app, request, abort

# Set up a logger for this module using a plain text formatter
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# Create a file handler that logs INFO messages
file_handler = logging.FileHandler("webhook.log")
file_handler.setLevel(logging.INFO)

# Create a logging format: timestamp - name - level - message
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
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
        
        # Log the GET request using a formatted string
        logger.info(
            "GET webhook verification request: mode=%s, token=%s, challenge=%s, remote_addr=%s, url=%s, extra_field=%s",
            mode, token, challenge, request.remote_addr, request.url, request.args.get('field')
        )
        
        if mode == 'subscribe' and token == VERIFY_TOKEN:
            logger.info("Webhook verified successfully")
            return challenge, 200
        else:
            logger.warning(
                "Verification token mismatch: mode=%s, token=%s, remote_addr=%s",
                mode, token, request.remote_addr
            )
            return 'Verification token mismatch', 403

    elif request.method == 'POST':
        data = request.get_json()
        # Log POST request details using string formatting
        logger.info(
            "POST webhook event received: method=%s, url=%s, remote_addr=%s, headers=%s, data=%s",
            request.method, request.url, request.remote_addr, dict(request.headers), data
        )
        return 'EVENT_RECEIVED', 200
