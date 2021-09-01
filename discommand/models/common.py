""" Common models shared throughout the discord api. """
from datetime import datetime, timezone, tzinfo

from ..constants.common import (
    SNOWFLAKE_INCREMENT_MASK,
    SNOWFLAKE_LENGTH,
    DISCORD_EPOCH,
    SNOWFLAKE_PROCESS_MASK,
    SNOWFLAKE_PROCESS_SHIFT,
    SNOWFLAKE_TIMESTAMP_SHIFT,
    SNOWFLAKE_WORKER_MASK,
    SNOWFLAKE_WORKER_SHIFT,
)


class Snowflake:
    """Twitter snowflake format.

    https://discord.com/developers/docs/reference#snowflakes
    """

    @classmethod
    def __get_validators__(cls):
        """Provide custom validators for pydantic."""

        yield cls.validate

    @classmethod
    def validate(cls, value):
        """Validate format of snowflake."""

        if not isinstance(value, str):
            raise TypeError("Snowflakes provided by the discord api are strings")

        try:
            num = int(value)
        except ValueError as error:
            raise ValueError(f"Snowflake strings must represent integers") from error

        if num > (1 << SNOWFLAKE_LENGTH):
            raise ValueError(
                f"Twitter snowflakes cannot be larger than {SNOWFLAKE_LENGTH} bits"
            )

        return cls(value)

    def __init__(self, value):
        self.value = value
        self.int = int(value)

    @property
    def timestamp(self) -> datetime:
        """Extract timestamp from snowflake."""

        timestamp = (self.int >> SNOWFLAKE_TIMESTAMP_SHIFT) + DISCORD_EPOCH

        return datetime.fromtimestamp(timestamp / 1000, tz=timezone.utc)

    @property
    def worker_id(self) -> int:
        """Extract worker_id from snowflake"""

        return (self.int & SNOWFLAKE_WORKER_MASK) >> SNOWFLAKE_WORKER_SHIFT

    @property
    def process_id(self) -> int:
        """Extract process_id from snowflake"""

        return (self.int & SNOWFLAKE_PROCESS_MASK) >> SNOWFLAKE_PROCESS_SHIFT

    @property
    def increment(self) -> int:
        """Extract increment value from snowflake"""

        return self.int & SNOWFLAKE_INCREMENT_MASK

    def __eq__(self, other) -> bool:
        if isinstance(other, str):
            return self.value == other
        if isinstance(other, int):
            return self.int == other
        if isinstance(other, Snowflake):
            return self.value == other.value and self.int == other.int

        raise NotImplementedError(
            f"Comparison between {type(other)} and {type(self)} not supported"
        )

    def __str__(self) -> str:
        return (
            "Snowflake "
            f"T:{self.timestamp.isoformat()} "
            f"W:{self.worker_id} "
            f"P:{self.process_id} "
            f"I:{self.increment}"
        )
