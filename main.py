from flask import Flask, request, jsonify
from slackeventsapi import SlackEventAdapter
from slack import WebClient
import os
import openai

# Initialize a Flask application
app = Flask(__name__)

signing_secret = "aea91a61cb57d809f34f6dde29ac2910"  # Replace with your actual signing_secret
slack_bot_token = "9X5tOX2GodKXch9bPNSbPR3h"  # Replace with your actual bot token

slack_events_adapter = SlackEventAdapter(signing_secret, "/slack/events", app)
slack_web_client = WebClient(token=slack_bot_token)

# OpenAI API key
openai.api_key = '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'

@app.route('/slack/command', methods=['POST'])
def handle_slash_command():
    command_text = request.form.get('text')
    response = call_gpt_3_api(command_text)

    # Send the response back to the channel
    response_channel = request.form.get('channel_id')
    slack_web_client.chat_postMessage(channel=response_channel, text=response)
    return '', 200

def call_gpt_3_api(prompt):
    try:
        # Create a chat models request
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo-16k-0613",
            messages=[
                {"role": "system", "content": "You are a helpful senior-level Oracle Database Developer."},
                {"role": "user", "content": prompt}
            ]
        )

        # Get the bot's message from the response
        bot_message = response['choices'][0]['message']['content']

        return bot_message

    except Exception as e:
        # If there was an error, return a message indicating the problem
        return f"Error: {str(e)}"

# Start the server
if __name__ == "__main__":
    app.run(port=3000)
