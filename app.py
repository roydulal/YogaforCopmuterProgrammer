import sys
from flask import Flask, request
from pprint import pprint
from pymessenger import Bot, Element
from utils import wit_response

app = Flask(__name__)

FB_ACCESS_TOKEN = "EAADrJVpQGToBAGYslyssJtsKVJZAjZAWZBw9AoquPVelaGsZCoaaN9ZAqvZBhnjZB3ZAacD0NUZAV4NZBOmaqPG7a4IActZA3SnvCyazv8RYMDDEcUaTOe9BZAQd9pdI2asZBitOKKbfJwZABlYUoVkkYM6v7ZA4lS53VpOFZC4JM2nZBvrQ5IgZDZD"
bot = Bot(FB_ACCESS_TOKEN)

VERIFICATION_TOKEN = "hello"


@app.route('/', methods=['GET'])
def verify():
    # Web hook verification
    if request.args.get("hub.mode") == "subscribe" and request.args.get("hub.challenge"):
        if not request.args.get("hub.verify_token") == "hello":
            return "Verification token mismatch", 403
        return request.args["hub.challenge"], 200
    return "Hello world", 200


@app.route('/', methods=['POST'])
def webhook():
    data = request.get_json()
    log(data)

    # Necessary Code that extract json data facebook send
    if data['object'] == 'page':
        for entry in data['entry']:
            for messaging_event in entry['messaging']:

                # IDs
                sender_id = messaging_event['sender']['id']
                recipient_id = messaging_event['recipient']['id']

                if messaging_event.get('message'):
                    # Extracting text message
                    if 'text' in messaging_event['message']:
                        messaging_text = messaging_event['message']['text']
                    else:
                        messaging_text = 'no text'

                    # replace Echo Bot to wit ai
                    response = None

                    entity, value = wit_response(messaging_text)

                    # if entity == 'greetings':
                    #     response = 'Welcome, Now we re in Testing, Please Contact Later'

                    if entity == 'greetings':
                        elements = []
                        element = Element(title="test", image_url="<arsenal_logo.png>", subtitle="subtitle",
                                          item_url="http://arsenal.com")
                        elements.append(element)

                        bot.send_generic_message(recipient_id, elements)

                    if response == None:
                        response = "Sorry, What is your Question, I didn't understand"

                    bot.send_text_message(sender_id, response)

    return "ok", 200


def log(message):
    # previously it was print now I just Use Petty Print
    pprint(message)
    sys.stdout.flush()


if __name__ == "__main__":
    app.run(use_reloader=True)
