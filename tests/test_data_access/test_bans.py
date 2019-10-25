import pytest
import datetime

from zeton.data_access import bans


def test_set_to_midnight():
    assert (bans.set_to_midnight(datetime.datetime(2019, 10, 25, 10, 10))) == datetime.datetime(2019, 10, 25, 0, 0)
