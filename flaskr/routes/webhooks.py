import logging
from flask import Blueprint, current_app, request, abort


# Set up a logger for this module using a plain text formatter
logger = logging.getLogger(__name__)


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
            "GET webhook verification request",
            extra={
                "mode": mode,
                "token": token,
                "challenge": challenge,
                "remote_addr": request.remote_addr,
                "url": request.url,
                "extra_field": request.args.get('field')
            }
        )
        
        if mode == 'subscribe' and token == VERIFY_TOKEN:
            logger.info("Webhook verified successfully")
            return challenge, 200
        else:
            logger.warning(
                "Verification token mismatch",
                extra={
                    "mode": mode,
                    "token": token,
                    "remote_addr": request.remote_addr
                }
            )
            return 'Verification token mismatch', 403

    elif request.method == 'POST':
        data = request.get_json()
        # Log POST request details using string formatting
        logger.info(
            "POST webhook event received",
            extra={
                "method": request.method,
                "url": request.url,
                "remote_addr": request.remote_addr,
                "headers": dict(request.headers),
                "data": data
            }
        )
        return 'EVENT_RECEIVED', 200
