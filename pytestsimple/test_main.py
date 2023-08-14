"""Simple test module."""
import main


def test_sum_to_n():
    """
    Test function sum_to_n with expected return correct result.
    :return: None
    """
    assert main.sum_to_n(5) == 10
