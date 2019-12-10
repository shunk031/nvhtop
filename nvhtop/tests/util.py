import os
from typing import List, Optional


def get_fake_stdin() -> Optional[List[str]]:
    fake_stdin_path = os.getenv("FAKE_STDIN_PATH", None)

    if fake_stdin_path is None:
        return None

    with open(fake_stdin_path, "rt") as rf:
        lines = [line.strip() for line in rf.readlines()]
    return lines
