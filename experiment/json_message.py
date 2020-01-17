import json
import os
import slack


def ChatPostJson(json_file_to_read = "./tmp/json_file.json"):
    json_file = open(json_file_to_read, "r")
    message_payload = json_file.read()

    web_client = slack.WebClient(token=os.environ['SLACK_BOT_TOKEN'])
    response = web_client.chat_postMessage(message_payload)

