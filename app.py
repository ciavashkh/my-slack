import os
from datetime import datetime
import time
import logging
import slack
import ssl as ssl_lib
import certifi
import message


@slack.RTMClient.run_on(event="message")

def handle_message(**payload):
    """Passing the message payload to message_handler
    .
    """
    handler_instance = message.MessageHandler(payload)
    handler_instance.handle()


if __name__ == "__main__":
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    logger.addHandler(logging.StreamHandler())
    ssl_context = ssl_lib.create_default_context(cafile=certifi.where())
    slack_token = os.environ["SLACK_BOT_TOKEN"]
    rtm_client = slack.RTMClient(token=slack_token, ssl=ssl_context)

# TO DO:
# { Find another way to get the bot's information
    BOT_INFORMARTION = slack.WebClient(token=os.environ['SLACK_BOT_TOKEN']).auth_test()
# }
    rtm_client.start()
