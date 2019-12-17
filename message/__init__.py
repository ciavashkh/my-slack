import logging
from logging import NullHandler

from message.message_handler import MessageHandler  # noqa

# Set default logging handler to avoid "No handler found" warnings.
logging.getLogger(__name__).addHandler(NullHandler())
