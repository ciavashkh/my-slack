import os
import time
from lib.schedule_message import *

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
            return "schedule a message"
        if text and (text.lower() == "list"):
            return "list schedules"
        if text and text.lower() == "goodbye":
            return "close connection"

    def handle(self):

        if ( self._action_required() == "schedule a message"):

            return schedule_a_message( 30, "your time is up", self.channel_id)

        if ( self._action_required() == "list schedules"):

            return list_schedules()

        if ( self._action_required() == "close connection"):

            rtm_client.stop()
