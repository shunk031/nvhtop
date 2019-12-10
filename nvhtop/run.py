#!/usr/bin/env python
import logging
import os
import sys

if os.environ.get("NVHTOP_DEBUG"):
    LEVEL = logging.DEBUG
else:
    LEVEL = logging.INFO

sys.path.insert(0, os.path.dirname(os.path.abspath(os.path.join(__file__, os.pardir))))
logging.basicConfig(
    format="%(asctime)s - %(levelname)s - %(name)s - %(message)s", level=LEVEL
)

from nvhtop.commands import main  # isort:skip # NOQA


def run():
    main(prog="nvidia-htop")


if __name__ == "__main__":
    run()
