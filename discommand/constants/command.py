""" Module for containing constants and other magic numbers. """

from enum import Enum

MAX_COMMAND_OPTIONS = 25
MAX_SUB_COMMAND_OPTIONS = 25

MAX_COMMAND_DESCRIPTION_LENGTH = 100
MAX_OPTION_DESCRIPTION_LENGTH = 100
MAX_CHOICE_NAME_LENGTH = 100
MAX_CHOICE_VALUE_LENGTH = 100
SNOWFLAKE_LENGTH = 64


class OptionType(int, Enum):
    """Data type for a command option.

    https://canary.discord.com/developers/docs/interactions/slash-commands#application-command-object-application-command-option-type
    """

    SUB_COMMAND = 1
    SUB_COMMAND_GROUP = 2
    STRING = 3
    INTEGER = 4
    BOOLEAN = 5
    USER = 6
    CHANNEL = 7
    ROLE = 8
    MENTIONABLE = 9
