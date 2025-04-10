import logging
from flask import Blueprint, current_app, request, abort

# Set up a logger for this module
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
# Create a file handler which logs INFO messages
file_handler = logging.FileHandler("webhook.log")
file_handler.setLevel(logging.INFO)
# Create a logging format
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)
# Add the handler to the logger
logger.addHandler(file_handler)

webhook_bp = Blueprint('webhook', __name__)

@webhook_bp.route('/webhook', methods=['GET', 'POST'])
def webhook():
    # Retrieve VERIFY_TOKEN from app config
    VERIFY_TOKEN = current_app.config.get('VERIFY_TOKEN')
    
    if request.method == 'GET':
        # Verification request from Meta
        mode = request.args.get('hub.mode')
        token = request.args.get('hub.verify_token')
        challenge = request.args.get('hub.challenge')
        
        if mode == 'subscribe' and token == VERIFY_TOKEN:
            logger.info("WEBHOOK_VERIFIED")
            print("WEBHOOK_VERIFIED")
            return challenge, 200
        else:
            logger.warning("Verification token mismatch: mode=%s, token=%s", mode, token)
            print("Verification token mismatch")
            return 'Verification token mismatch', 403

    elif request.method == 'POST':
        # Event notification from Meta's API
        data = request.get_json()
        logger.info("Received event: %s", data)
        print("Received event:")
        print(data)
        # Here you can add additional processing logic (e.g., storing data in a database)
        return 'EVENT_RECEIVED', 200