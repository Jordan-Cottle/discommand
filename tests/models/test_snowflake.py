""" Test module for snowflake parseing and validation. """

from datetime import datetime, timezone

import pytest

from discommand.models.common import Snowflake


EXAMPLE_DATA = "175928847299117063"
EXAMPLE_DATETIME = datetime(
    year=2016,
    month=4,
    day=30,
    hour=11,
    minute=18,
    second=25,
    microsecond=796000,
    tzinfo=timezone.utc,
)
EXAMPLE_WORKER_ID = 1
EXAMPLE_PROCESS_ID = 0
EXAMPLE_INCREMENT = 7


@pytest.fixture(name="example_snowflake")
def create_example_snowflake():
    """Create example snowflake from example data."""

    return Snowflake(EXAMPLE_DATA)


def test_example_snowflake(example_snowflake):
    """Ensure the example snowflake parses properly."""

    assert (
        example_snowflake.timestamp == EXAMPLE_DATETIME
    ), f"{example_snowflake} off by {example_snowflake.timestamp - EXAMPLE_DATETIME}"

    assert example_snowflake.worker_id == EXAMPLE_WORKER_ID
    assert example_snowflake.process_id == EXAMPLE_PROCESS_ID
    assert example_snowflake.increment == EXAMPLE_INCREMENT

    assert str(example_snowflake) == (
        "Snowflake "
        f"T:{EXAMPLE_DATETIME.isoformat()} "
        f"W:{EXAMPLE_WORKER_ID} "
        f"P:{EXAMPLE_PROCESS_ID} "
        f"I:{EXAMPLE_INCREMENT}"
    )


@pytest.mark.parametrize(
    "other_value,expected_result",
    [
        (EXAMPLE_DATA, True),
        (int(EXAMPLE_DATA), True),
        (Snowflake(EXAMPLE_DATA), True),
        ("foo", False),
        (42, False),
        (Snowflake("123567423178"), False),
    ],
)
def test_snowflake_equals(example_snowflake, other_value, expected_result):
    """Ensure equals methods can be used for multipel types."""

    assert (example_snowflake == other_value) == expected_result


def test_snowflake_equals_unexpected_type(example_snowflake):
    """Ensure un implemented comparisons complain"""

    with pytest.raises(NotImplementedError):
        example_snowflake == datetime.now()
