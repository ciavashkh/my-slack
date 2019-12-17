import os
import time
import slack

def schedule_a_message(time_length:int, text:str, channel:str):
    
    web_client = slack.WebClient(token=os.environ['SLACK_BOT_TOKEN'])

    message_scheduled_at = int(time.time() + time_length)
    extra_elements = {'channel': channel, 'post_at': message_scheduled_at, 'text': text}

    message_payload = {}
    message_payload.update(extra_elements)
    response = web_client.chat_scheduleMessage(**message_payload)

    return

def list_schedules():

    web_client = slack.WebClient(token=os.environ['SLACK_BOT_TOKEN'])
    response = web_client.chat_scheduledMessages_list()

    return