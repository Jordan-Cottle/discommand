""" Test module for user models. """

from itertools import combinations

import pytest

from discommand.constants.user import UserFlag
from discommand.models.user import User, UserFlags


# https://canary.discord.com/developers/docs/resources/user#user-object-example-user
EXAMPLE_USER = {
    "id": "80351110224678912",
    "username": "Nelly",
    "discriminator": "1337",
    "avatar": "8342729096ea3675442027381ff50dfe",
    "verified": True,
    "email": "nelly@discord.com",
    "flags": 64,
    "premium_type": 1,
    "public_flags": 64,
}


@pytest.fixture(name="user_data")
def copy_user_data():
    """Provide copy of user data so tests can modify it safely."""

    return EXAMPLE_USER.copy()


def test_example_user(user_data):
    """Ensure example from discord docs is parsable."""

    user = User.parse_obj(user_data)

    assert user.id == "80351110224678912"
    assert user.username == "Nelly"
    assert user.discriminator == "1337"
    assert user.avatar == "8342729096ea3675442027381ff50dfe"
    assert user.verified
    assert user.email == "nelly@discord.com"
    assert user.flags == 64
    assert user.premium_type == 1
    assert user.public_flags == 64


def test_example_user_flags(user_data):
    """Test names attributes on user flags for example user."""

    user_flags = UserFlags(user_data["flags"])

    assert not user_flags.none
    assert not user_flags.discord_employee
    assert not user_flags.partnered_server_owner
    assert not user_flags.hypesquad_events
    assert not user_flags.bug_hunter_level_1
    assert not user_flags.bug_hunter_level_2
    assert user_flags.house_bravery
    assert not user_flags.house_brilliance
    assert not user_flags.house_balance
    assert not user_flags.early_supporter
    assert not user_flags.team_user
    assert not user_flags.verified_bot
    assert not user_flags.early_verified_bot_developer
    assert not user_flags.discord_certified_moderator


@pytest.mark.deep
@pytest.mark.parametrize(
    "set_flags",
    [
        combination
        for i in range(1, len(UserFlag))
        for combination in combinations(UserFlag, i)
        if UserFlag.NONE not in combination
    ],
)
def test_user_flags(set_flags):
    """Throughoughly test all combinations of flags."""

    user_flags = UserFlags(sum(set_flags))

    print(f"Testing attribuite access for {set_flags}")

    for flag in UserFlag:
        if flag in set_flags:
            assert getattr(user_flags, flag.name)
            assert getattr(user_flags, flag.name.upper())
            assert getattr(user_flags, flag.name.lower())
        else:
            assert not getattr(user_flags, flag.name)
            assert not getattr(user_flags, flag.name.upper())
            assert not getattr(user_flags, flag.name.lower())
