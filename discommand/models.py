""" A simple Command class to register new commands for a discord bot. """

import re
from typing import List, Optional, Sequence, Union

from pydantic import BaseModel, ConstrainedStr, validator

from .constants import (
    MAX_CHOICE_NAME_LENGTH,
    MAX_CHOICE_VALUE_LENGTH,
    MAX_COMMAND_DESCRIPTION_LENGTH,
    MAX_COMMAND_OPTIONS,
    MAX_OPTION_DESCRIPTION_LENGTH,
    MAX_SUB_COMMAND_OPTIONS,
    SNOWFLAKE_LENGTH,
    OptionType,
)


class Snowflake(ConstrainedStr):
    """Twitter snowflake format.

    https://discord.com/developers/docs/reference#snowflakes
    """

    min_length = SNOWFLAKE_LENGTH
    max_length = SNOWFLAKE_LENGTH


class CommandName(ConstrainedStr):
    """Constrained string for command names."""

    regex = re.compile(r"^[\w-]{1,32}$")


class OptionName(ConstrainedStr):
    """Constrained string for option names."""

    regex = re.compile(r"^[\w-]{1,32}$")


class ChoiceName(ConstrainedStr):
    """Constrained string for choice names"""

    min_length = 1
    max_length = MAX_CHOICE_NAME_LENGTH

    # TODO Does discord have any more constraints beyond just length?


class CommandDescription(ConstrainedStr):
    """Constrained string for command descriptions."""

    min_length = 1
    max_length = MAX_COMMAND_DESCRIPTION_LENGTH


class OptionDescription(ConstrainedStr):
    """Constrained string for command option descriptions."""

    min_length = 1
    max_length = MAX_OPTION_DESCRIPTION_LENGTH


class ChoiceString(ConstrainedStr):
    """Constrained string for choice values."""

    max_length = MAX_CHOICE_VALUE_LENGTH


class Choice(BaseModel):
    """Value for an option with a set number of choices.

    https://canary.discord.com/developers/docs/interactions/slash-commands#application-command-object-application-command-option-choice-structure
    """

    name: ChoiceName
    value: Union[int, ChoiceString]


class Option(BaseModel):
    """Option for a command.

    https://canary.discord.com/developers/docs/interactions/slash-commands#application-command-object-application-command-option-structure
    """

    type: OptionType
    name: OptionName
    description: OptionDescription
    required: bool = False
    choices: Optional[Sequence[Choice]]
    options: Optional[Sequence["Option"]]

    @validator("options")
    @classmethod  # Pylint doesn't know @validator does this already
    # https://github.com/PyCQA/pylint/issues/1694
    def validate_options(cls, options, values):
        """Ensure that options are only supplied for subcommand options."""

        if values["type"] not in {OptionType.SUB_COMMAND, OptionType.SUB_COMMAND_GROUP}:
            raise ValueError("Options can only be supplied for sub commands.")

        if len(options) > MAX_SUB_COMMAND_OPTIONS:
            raise ValueError(
                f"Subcommand can only have up to {MAX_SUB_COMMAND_OPTIONS} options"
            )

        return options


# This is to resolve the Optional[Sequence["Option"]] type hint into Optional[Sequence[Option]]
Option.update_forward_refs()


class Command(BaseModel):
    """A command that a user can execute.

    https://canary.discord.com/developers/docs/interactions/slash-commands#application-command-object-application-command-structure
    """

    id: Optional[Snowflake]
    application_id: Optional[Snowflake]
    guid: Optional[Snowflake]
    name: CommandName
    description: CommandDescription
    options: Optional[List[Option]]
    default_permission: Optional[bool] = True

    @validator("options")
    @classmethod  # https://github.com/PyCQA/pylint/issues/1694
    def validate_options(cls, options: List[Option]):
        """Validate number and order of options."""

        if len(options) > MAX_COMMAND_OPTIONS:
            raise ValueError(f"A command can only have {MAX_COMMAND_OPTIONS} options")

        sorted_options = sorted(
            options, key=lambda option: option.required, reverse=True
        )
        if sorted_options != options:
            raise ValueError(
                "Discord api requires required options to be specified before optional ones"
            )

        return options
