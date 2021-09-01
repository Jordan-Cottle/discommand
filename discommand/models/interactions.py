""" Models related to the interactions api. """

from typing import Mapping, Optional, Sequence, Union

from pydantic import BaseModel

from ..constants import InteractionType, OptionType
from .common import Snowflake
from .command import CommandName, OptionName
from .user import User


class InteractionDataOption(BaseModel):
    """Data format for supplied interaction option information."""

    name: OptionName
    type: OptionType
    value: Optional[Union[int, str]]
    options: Optional[Sequence["InteractionDataOption"]]


# Resolve Optional[Sequence["InteractionDataOption"]]
InteractionDataOption.update_forward_refs()


class InteractionDataResolved(BaseModel):
    """Data container for resolved users, roles, and channels."""

    users: Optional[Mapping[Snowflake, User]]
    members: Optional[Mapping[Snowflake, "PartialMember"]]
    roles: Optional[Mapping[Snowflake, "Role"]]
    channels: Optional[Mapping[Snowflake, "PartialChannel"]]


class InteractionData(BaseModel):
    """Data format for interaction data."""

    id: Snowflake
    name: CommandName
    resolved: Optional[InteractionDataResolved]
    options: Optional[Sequence[InteractionDataOption]]
    custom_id: str
    component_type: "ComponentType"


class IncomingInteraction(BaseModel):
    """Format of incoming interaction data."""

    id: Snowflake
    application_id: Snowflake
    type: InteractionType
    data: Optional[InteractionData]
    guild_id: Optional[Snowflake]
    channel_id: Optional[Snowflake]
    member: Optional["GuildMember"]
    user: Optional[User]
    token: str
    version: int
    message: Optional["Message"]
