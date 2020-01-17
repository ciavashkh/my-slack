import os
import time
from lib.messaging import *
from experiment.json_message import *

class MessageHandler:

    def __init__(self, payload):
        self.data = payload["data"]
        self.channel_id = self.data.get("channel")
        self.user_id = self.data.get("user")
        self.text = self.data.get("text")
        self.message_ts = float(self.data.get("ts"))

    def _action_required(self):
        text = self.text
        if text and (text.lower() == "start"):
            return {'action': "schedule a message", 'time_length' : 3000}
        if text and (text.lower() == "experiment"):
            return {'action': "experiment"}
        if text and (text.lower() == "list"):
            return {'action': "list schedules", 'channel_id' : self.channel_id}
        if text and text.lower() == "goodbye":
            return {'action': "close connection"}

        return {'action': "no action"}

    def handle(self):

        action_info = self._action_required()


        if (action_info["action"] == "schedule a message"):
            return message_schedule( action_info["time_length"], "your time is up", self.channel_id)

        if (action_info["action"] == "list schedules"):
            return message_schedule_list(action_info["channel_id"])

        if (action_info["action"] == "experiment"):
            return ChatPostJson()

        if ( self._action_required() == "close connection"):
            rtm_client.stop()


        return

