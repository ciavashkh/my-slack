import os
from datetime import datetime
import time
import logging
import slack
import ssl as ssl_lib
import certifi
from scheduled_message import ScheduledMessage
from messaging import Communication

# For simplicity we'll store our app data in-memory with the following data structure.
# scheduled_message_sent = {"channel": {"user_id": OnboardingTutorial}}
message_sent = {}
scheduled_message_sent = {}
def greeting(web_client: slack.WebClient, user_id: str, channel: str):
    # Create a new communication.
    communication = Communication(channel)
    
    print ("first_communication is: \n", dir(communication))
    # Get the onboarding e payload
    message = communication.get_message_payload()
    print ("First_message is: \n", message)
    # Post the onboarding message in Slack
    response = web_client.chat_postMessage(**message)

    # Capture the timestamp of the message we've just posted so
    # we can use it to update the message after a user
    # has completed an onboarding task.
    communication.timestamp = response["ts"]
    print ("TIMESTAMP is: \n", communication.timestamp)

    # Store the message sent in messaging_sent
    if channel not in message_sent:
        message_sent[channel] = {}
    message_sent[channel][user_id] = communication

    print ("messaege_sent is: \n", message_sent)

def time_deference(start_time, end_time=time.time()):
    return (end_time - start_time)/3600

def file_modified_time(path_to_file):
    stat = os.stat(path_to_file)
    return stat.st_mtime


def schdule_a_message(web_client: slack.WebClient, user_id: str, channel: str, message_arrived_at: int , usre_id: str):
    # Create a new onboarding tutorial.
    
    communication = Communication(channel)
    first_message = communication.get_message_payload()
    message1_timestamp = int(message_arrived_at + 20)
    text_message = "Greetings"
    extra_elements = {'post_at': message1_timestamp, 'text': text_message}
    first_message.update(extra_elements)
    scheduled_message = ScheduledMessage(channel)

    # Get the onboarding message payload
    message = scheduled_message.get_message_payload()
    # print ("second Message is: \n",first_message)
    # Post the onboarding message in Slack
    response = web_client.chat_scheduleMessage(**first_message)

    # Capture the timestamp of the message we've just posted so
    # we can use it to update the message after a user
    # has completed an onboarding task.
    scheduled_message.timestamp = response["ts"]
    # print ("TIMESTAMP is: \n", scheduled_message.timestamp)
    # print ("Response is: \n", response)

    # Store the message sent in scheduled_message_sent
    if channel not in scheduled_message_sent:
        scheduled_message_sent[channel] = {}
    scheduled_message_sent[channel][user_id] = scheduled_message


# ============== Message Events ============= #
# When a user sends a DM, the event type will be 'message'.
# Here we'll link the message callback to the 'message' event.
@slack.RTMClient.run_on(event="message")
def message(**payload):
    """Display the onboarding welcome message after receiving a message
    that contains "start".
    """
    print ("the data is: \n", payload)
    data = payload["data"]
    web_client = payload["web_client"]
    channel_id = data.get("channel")
    user_id = data.get("user")
    text = data.get("text")
    message_ts = float(data.get("ts"))

    if text and (text.lower() == "morning" or text.lower() == "good morning"):
        return schdule_a_message(web_client, user_id, channel_id, message_ts, user_id)
    if text and text.lower() == "goodbye":
        rtm_client.stop()


if __name__ == "__main__":
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    logger.addHandler(logging.StreamHandler())
    ssl_context = ssl_lib.create_default_context(cafile=certifi.where())
    slack_token = os.environ["SLACK_BOT_TOKEN"]
    rtm_client = slack.RTMClient(token=slack_token, ssl=ssl_context)
    rtm_client.start()
