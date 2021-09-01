""" Constants needed by interactions componenents. """

from enum import Enum


class InteractionType(int, Enum):
    """Types of incoming interaction."""

    PING = 1
    APPLICATION_COMMAND = 2
    MESSAGE_COMPONENT = 3


class InteractionResponseType(int, Enum):
    """Types of interaction responses."""

    PONG = 1
    CHANNEL_MESSAGE_WITH_SOURCE = 4
    DEFERRED_CHANNEL_MESSAGE_WITH_SOURCE = 5
    DEFERRED_UPDATE_MESSAGE = 6
    UPDATE_MESSAGE = 7


PONG = {"type": InteractionResponseType.PONG}
