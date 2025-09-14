from flask import Flask, render_template, request, jsonify
import requests
import json
import logging

app = Flask(__name__, template_folder='templates')

# URL of the Rasa server's REST API endpoint
RASA_API_URL = 'http://rasa-bot:5005/webhooks/rest/webhook'

# Configure logging
logging.basicConfig(level=logging.INFO)

@app.route('/')
def home():
    """Renders the main chatbot HTML page."""
    return render_template('index.html')

@app.route('/webhook', methods=['POST'])
def webhook():
    """Handles incoming messages from the user and sends them to the Rasa bot."""
    user_message = request.json.get('message')
    logging.info(f"Received user message: {user_message}")

    try:
        # Send the user message to the Rasa bot
        rasa_response = requests.post(
            RASA_API_URL,
            json={"sender": "user", "message": user_message},
            headers={"Content-Type": "application/json"}
        )
        rasa_response.raise_for_status() # Raise an exception for bad status codes
        
        # Get the bot's response
        bot_response = rasa_response.json()
        logging.info(f"Rasa bot response: {bot_response}")

        return jsonify(bot_response)

    except requests.exceptions.RequestException as e:
        logging.error(f"Error communicating with Rasa server: {e}")
        return jsonify([{"text": "I'm sorry, I am currently unable to respond. Please try again later."}]), 503
    except json.JSONDecodeError as e:
        logging.error(f"Error decoding JSON from Rasa response: {e}")
        return jsonify([{"text": "I encountered an error processing the response."}]), 500
    except Exception as e:
        logging.error(f"An unexpected error occurred: {e}")
        return jsonify([{"text": "An unexpected error occurred."}]), 500

if __name__ == '__main__':
    # Using 0.0.0.0 as the host is necessary for Docker container to be accessible
    app.run(host='0.0.0.0', port=5000)
