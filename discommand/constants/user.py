""" Constants relating to users and roles. """

from enum import Enum

DISCRIMINATOR_LENGTH = 4


class UserFlag(int, Enum):
    """Flags that can be set for a user."""

    NONE = 0
    DISCORD_EMPLOYEE = 1 << 0
    PARTNERED_SERVER_OWNER = 1 << 1
    HYPESQUAD_EVENTS = 1 << 2
    BUG_HUNTER_LEVEL_1 = 1 << 3
    HOUSE_BRAVERY = 1 << 6
    HOUSE_BRILLIANCE = 1 << 7
    HOUSE_BALANCE = 1 << 8
    EARLY_SUPPORTER = 1 << 9
    TEAM_USER = 1 << 10
    BUG_HUNTER_LEVEL_2 = 1 << 14
    VERIFIED_BOT = 1 << 16
    EARLY_VERIFIED_BOT_DEVELOPER = 1 << 17
    DISCORD_CERTIFIED_MODERATOR = 1 << 18


class PremiumType(int, Enum):
    """Types of premium users."""

    NONE = 0
    NITRO_CLASSIC = 1
    NITRO = 2
