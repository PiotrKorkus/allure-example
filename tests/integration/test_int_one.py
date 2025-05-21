import logging
import pytest

def test_success(fixture_integration):
    """_summary_
    Args:
        fixture_integration (_type_): _description_
    """
    logging.info(fixture_integration)
    assert fixture_integration == "integration"

def test_failure():
    assert False

@pytest.mark.xfail(raises=RuntimeError)
def test_xfailure():
    raise RuntimeError