""" Data validation tests for command models."""

from copy import deepcopy

import pytest
from pydantic import ValidationError

from discommand.constants.command import (
    MAX_CHOICE_NAME_LENGTH,
    MAX_CHOICE_VALUE_LENGTH,
    MAX_COMMAND_DESCRIPTION_LENGTH,
    MAX_COMMAND_OPTIONS,
    MAX_OPTION_DESCRIPTION_LENGTH,
    MAX_SUB_COMMAND_OPTIONS,
    OptionType,
)
from discommand.models import Choice, Command, Option

# https://canary.discord.com/developers/docs/interactions/slash-commands#registering-a-command
EXAMPLE_JSON = {
    "name": "blep",
    "description": "Send a random adorable animal photo",
    "options": [
        {
            "name": "animal",
            "description": "The type of animal",
            "type": 3,
            "required": True,
            "choices": [
                {"name": "Dog", "value": "animal_dog"},
                {"name": "Cat", "value": "animal_cat"},
                {"name": "Penguin", "value": "animal_penguin"},
            ],
        },
        {
            "name": "only_smol",
            "description": "Whether to show only baby animals",
            "type": 5,
            "required": False,
        },
    ],
}

SUB_COMMAND_WITH_OPTIONS = {
    "name": "sub_command",
    "type": OptionType.SUB_COMMAND,
    "description": "Another command underneath the main command.",
    "options": [
        {
            "name": "verbose",
            "type": OptionType.BOOLEAN,
            "description": "Provide more verbose output.",
        }
    ],
}


@pytest.fixture(name="example_data")
def copy_example_data():
    """Copy test data so tests can safely modify it"""

    return deepcopy(EXAMPLE_JSON)


@pytest.fixture(name="sub_command_data")
def copy_sub_command_data():
    """Copy test data so tests can safely modify it"""

    return deepcopy(SUB_COMMAND_WITH_OPTIONS)


def assert_has_error_for(error: ValidationError, name: str):
    """Assert that the validation error mentions a specific name."""

    assert any(name in error_item["loc"] for error_item in error.errors())


def test_valid_command(example_data):
    """Ensure a valid command passes all checks."""

    command = Command.parse_obj(example_data)

    assert command.name == "blep"
    assert command.description == "Send a random adorable animal photo"
    assert len(command.options) == 2

    option_1, option_2 = command.options
    assert option_1.name == "animal"
    assert option_1.description == "The type of animal"
    assert option_1.type == OptionType.STRING
    assert option_1.required
    assert len(option_1.choices) == 3

    choice_1, choice_2, choice_3 = option_1.choices
    assert choice_1.name == "Dog"
    assert choice_1.value == "animal_dog"
    assert choice_2.name == "Cat"
    assert choice_2.value == "animal_cat"
    assert choice_3.name == "Penguin"
    assert choice_3.value == "animal_penguin"

    assert option_2.name == "only_smol"
    assert option_2.description == "Whether to show only baby animals"
    assert option_2.type == OptionType.BOOLEAN
    assert not option_2.required
    assert option_2.choices is None


def test_bad_command_name(example_data):
    """Test model validates names."""

    example_data["name"] = "foo23!"

    with pytest.raises(ValidationError) as exc_info:
        Command.parse_obj(example_data)

    assert_has_error_for(exc_info.value, "name")


@pytest.mark.parametrize(
    "description", ["", "a" * (MAX_COMMAND_DESCRIPTION_LENGTH + 1)]
)
def test_bad_command_description(example_data, description):
    """Test model validates names."""

    example_data["description"] = description

    with pytest.raises(ValidationError) as exc_info:
        Command.parse_obj(example_data)

    assert_has_error_for(exc_info.value, "description")


@pytest.mark.parametrize(
    "options",
    [
        # Too many options
        [
            {
                "name": "animal",
                "description": "The type of animal",
                "type": OptionType.STRING,
            }
        ]
        * (MAX_COMMAND_OPTIONS + 1),
        # Description too long
        [
            {
                "name": "animal",
                "description": "a" * (MAX_OPTION_DESCRIPTION_LENGTH + 1),
                "type": OptionType.STRING,
            }
        ],
        # Out of order options (required should come first)
        [
            {
                "name": "animal",
                "description": "The type of animal",
                "type": OptionType.STRING,
            },
            {
                "name": "animal",
                "description": "The type of animal",
                "type": OptionType.STRING,
                "required": True,
            },
        ],
    ],
)
def test_bad_command_options(example_data, options):
    """Ensure command options validator rejects bad sequences of commands."""
    example_data["options"] = options

    with pytest.raises(ValidationError) as exc_info:
        Command.parse_obj(example_data)

    assert_has_error_for(exc_info.value, "options")


@pytest.mark.parametrize(
    "option",
    [
        {
            "name": "animal",
            "description": "The type of animal",
            "type": OptionType.STRING,
            "required": True,
            "options": [
                {
                    "name": "action",
                    "description": "The type of action the animal should do",
                    "type": OptionType.STRING,
                }
            ],
        },
        {
            "name": "sub_command",
            "description": "The sub command to perform",
            "type": OptionType.SUB_COMMAND,
            "required": True,
            "options": [
                {
                    "name": "animal",
                    "description": "The type of animal",
                    "type": OptionType.STRING,
                }
            ]
            * (MAX_SUB_COMMAND_OPTIONS + 1),
        },
    ],
)
def test_bad_sub_command_options(option):
    """Ensure sub command options are validated."""

    with pytest.raises(ValidationError) as exc_info:
        Option.parse_obj(option)

    assert_has_error_for(exc_info.value, "options")


def test_sub_command_valid_options(sub_command_data):
    """Test that a valid sub command with options works."""

    option = Option.parse_obj(sub_command_data)

    assert option.name == "sub_command"
    assert option.type == OptionType.SUB_COMMAND
    assert option.description == "Another command underneath the main command."
    assert len(option.options) == 1

    sub_option = option.options[0]
    assert sub_option.name == "verbose"
    assert sub_option.type == OptionType.BOOLEAN
    assert sub_option.description == "Provide more verbose output."


@pytest.mark.parametrize(
    "choice_data",
    [
        {
            "name": "",
            "value": 1,
        },
        {
            "name": "a" * (MAX_CHOICE_NAME_LENGTH + 1),
            "value": 2,
        },
    ],
)
def test_bad_choice_name(choice_data):
    """Ensure bad choice names are validated."""

    with pytest.raises(ValidationError) as exc_info:

        Choice.parse_obj(choice_data)

    assert_has_error_for(exc_info.value, "name")


@pytest.mark.parametrize(
    "choice_data",
    [
        {
            "name": "one",
            "value": None,
        },
        {
            "name": "two",
            "value": "a" * (MAX_CHOICE_VALUE_LENGTH + 1),
        },
    ],
)
def test_bad_choice_value(choice_data):
    """Ensure bad choice names are validated."""

    with pytest.raises(ValidationError) as exc_info:

        Choice.parse_obj(choice_data)

    assert_has_error_for(exc_info.value, "value")


@pytest.mark.parametrize("name,value", [("one", 1), ("hello", "world")])
def test_valid_choice(name, value):
    """Test valid choices can be constructed."""

    choice = Choice.parse_obj({"name": name, "value": value})

    assert choice.name == name
    assert choice.value == value
