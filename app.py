import os
from flask import Flask, request
from twilio.rest import TwilioRestClient

app = Flask(__name__)

# Find these values at https://twilio.com/user/account
account_sid = os.environ['TWILIO_ACCOUNT_SID']
auth_token = os.environ['TWILIO_AUTH_TOKEN']
client = TwilioRestClient(account_sid, auth_token)


@app.route("/", methods=['POST'])
def send_sms():
    event_json = request.get_json()
    amount = event_json['data']['object']['amount']
    location = event_json['data']['object']['source']['address_state']
    message_body = "Hey! Your shop just recieved an order for $"
        + '{:20,.2f}'.format(amount) + " in " + location + "."
    message = client.messages.create(to=os.environ['PHONE_NUMBER'],
                                     from_=os.environ['TWILIO_NUMBER'],
                                     body=message_body)
    return '', 200


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
