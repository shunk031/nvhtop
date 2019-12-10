import re
from copy import deepcopy
from typing import List

from termcolor import colored


class Colorizer(object):

    PAT = re.compile(
        r"\| (?:N/A|..%)\s+[0-9]{2,3}C.*\s([0-9]+)MiB\s+\/\s+([0-9]+)MiB.*\s([0-9]+)%"
    )

    def __init__(
        self,
        memory_free_ratio: float = 0.05,
        gpu_free_ratio: float = 0.05,
        memory_moderate_ratio: float = 0.9,
        gpu_moderate_ratio: float = 0.75,
    ) -> None:

        self._memory_free_ratio = memory_free_ratio
        self._gpu_free_ratio = gpu_free_ratio
        self._memory_moderate_ratio = memory_moderate_ratio
        self._gpu_moderate_ratio = gpu_moderate_ratio

    def _get_used_mem(self, m: re.Match) -> int:
        return int(m.group(1))

    def _get_total_mem(self, m: re.Match) -> int:
        return int(m.group(2))

    def _get_gpu_util(self, m: re.Match) -> int:
        return int(m.group(3)) / 100.0

    def _colorize_lines(self, lines: str) -> str:

        for i in range(len(lines)):
            line = lines[i]
            m = self.PAT.match(line)
            if m is not None:
                used_mem = self._get_used_mem(m)
                total_mem = self._get_total_mem(m)
                gpu_util = self._get_gpu_util(m)
                mem_util = used_mem / float(total_mem)

                is_moderate = False
                is_high = (
                    gpu_util >= self._gpu_moderate_ratio
                    or mem_util >= self._memory_moderate_ratio
                )
                if not is_high:
                    is_moderate = (
                        gpu_util >= self._gpu_free_ratio
                        or mem_util >= self._memory_free_ratio
                    )

                c = "red" if is_high else ("yellow" if is_moderate else "green")
                lines[i] = colored(lines[i], c)
                lines[i - 1] = colored(lines[i - 1], c)

        return lines

    def colorize(self, lines: List[str]) -> List[str]:

        lines = deepcopy(lines)
        lines = self._colorize_lines(lines)
        return lines
