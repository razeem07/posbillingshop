from twilio.rest import Client

account_sid = 'AC5c5608b9eda1791cabb0f448d7830d85'

auth_token = '667c4de7d2e966b8af7310e048264bdf'

client = Client(account_sid, auth_token)

message = client.messages.create(
    from_='8281750375',
    to='[8281750375]',body="hi"
)
print(message.sid)