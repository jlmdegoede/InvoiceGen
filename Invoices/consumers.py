from channels import Channel
from channels.sessions import channel_session
import json
from .tasks import generate_pdf_task

@channel_session
def ws_connect(message):
    message.reply_channel.send({
        "text": json.dumps({
            "action": "reply_channel",
            "reply_channel": message.reply_channel.name,
        })
    })

@channel_session
def ws_receive(message):
    data = json.loads(message['text'])
    reply_channel = message.reply_channel.name

    if data['action'] == "start_pdf":
        start_pdf(data['invoice_id'], reply_channel)

def start_pdf(invoice_id, reply_channel):
    generate_pdf_task.delay(invoice_id, reply_channel)

    Channel(reply_channel).send({
        "text": json.dumps({
            "action": "started",
        })
    })