from ..constants.common import SNOWFLAKE_LENGTH

from pydantic.types import ConstrainedStr


class Snowflake(ConstrainedStr):
    """Twitter snowflake format.

    https://discord.com/developers/docs/reference#snowflakes
    """

    min_length = SNOWFLAKE_LENGTH
    max_length = SNOWFLAKE_LENGTH
