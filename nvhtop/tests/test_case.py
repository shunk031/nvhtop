import pathlib
from unittest import TestCase


class NvHtopTestCase(TestCase):
    PROJECT_ROOT = (pathlib.Path(__file__).parent / ".." / "..").resolve()
    MODULE_ROOT = PROJECT_ROOT / "nvhtop"
    TESTS_ROOT = MODULE_ROOT / "tests"
    FIXTURES_ROOT = TESTS_ROOT / "fixtures"
