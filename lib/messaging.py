import os
import time
import slack

def message_post(text:str, channel:str):

	web_client = slack.WebClient(token=os.environ['SLACK_BOT_TOKEN'])

	essential_elements = {'channel': channel, 'text': text}

	message_payload = {}
	message_payload.update(essential_elements)

	response = web_client.chat_postMessage(**message_payload)

	return


def message_schedule(time_length:int, text:str, channel:str):
    
    web_client = slack.WebClient(token=os.environ['SLACK_BOT_TOKEN'])

    message_scheduled_at = int(time.time() + time_length)
    essential_elements = {'channel': channel, 'post_at': message_scheduled_at, 'text': text}

    message_payload = {}
    message_payload.update(essential_elements)
    response = web_client.chat_scheduleMessage(**message_payload)

    return

def message_schedule_list(channel_id:str):

    web_client = slack.WebClient(token=os.environ['SLACK_BOT_TOKEN'])
    response = web_client.chat_scheduledMessages_list()

    has_schedules = response["scheduled_messages"]

    print("cia response", scheduled_messages)

    if has_schedules :
        for item in response["scheduled_messages"]:

        	message_post(item, channel_id)

    return

