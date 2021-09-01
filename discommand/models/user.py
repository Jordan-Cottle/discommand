""" Models relating to users and roles. """

import re
from typing import Optional

from pydantic import BaseModel, ConstrainedStr
from pydantic.types import ConstrainedInt

from ..constants.user import DISCRIMINATOR_LENGTH, UserFlag, PremiumType
from .common import Snowflake


class Discriminator(ConstrainedStr):
    """4 digit discord tag for a user"""

    regex = re.compile(fr"\d{{{DISCRIMINATOR_LENGTH}}}")


class AvatarHash(ConstrainedStr):
    """Hash to identify a user's avatar.

    https://canary.discord.com/developers/docs/reference#image-formatting
    """

    # TODO: can we make this stricter?
    # Are there more/less charaters to allow?
    # Is there a length limit?
    regex = re.compile(r"[\w\d]+")


class UserFlags(ConstrainedInt):
    """Flags on a user's account.

    https://canary.discord.com/developers/docs/resources/user#user-object-user-flags
    """

    max_value = sum(UserFlag)

    def __getattr__(self, name):
        """Dynamically provide attributes for use flags."""

        try:
            return bool(self & UserFlag[name.upper()])
        except KeyError:
            raise AttributeError(f"{name} is not a possible user flag")

    # List of UserFlag names for editor auto complete
    none: bool
    discord_employee: bool
    partnered_server_owner: bool
    hypesquad_events: bool
    bug_hunter_level_1: bool
    house_bravery: bool
    house_brilliance: bool
    house_balance: bool
    early_supporter: bool
    team_user: bool
    bug_hunter_level_2: bool
    verified_bot: bool
    early_verified_bot_developer: bool
    discord_certified_moderator: bool


class User(BaseModel):
    """Represents a discord user (including bots).

    https://canary.discord.com/developers/docs/resources/user#user-object-user-structure
    """

    id: Snowflake
    username: str
    discriminator: Discriminator
    avatar: AvatarHash
    bot: Optional[bool]
    system: Optional[bool]
    mfa_enabled: Optional[bool]
    locale: Optional[str]
    verified: Optional[bool]
    email: Optional[str]
    flags: Optional[UserFlags]
    premium_type: Optional[PremiumType]
    public_flags: Optional[UserFlags]
