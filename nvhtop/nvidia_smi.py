import re
import select
import subprocess
import sys
from typing import List

from nvhtop.process import GPUProcess
from nvhtop.tests.util import get_fake_stdin
from nvhtop.util import Colorizer


class NvidiaSmi(object):
    COMMAND = "nvidia-smi"
    NO_RUNNING_PROCESS = "No running processes found"
    NOT_SUPPORTED = "Not Supported"
    PROCESSES_START = "| Processes:"
    PATTERN = re.compile(r"\s+")

    def __init__(self, is_color: bool = False) -> None:
        self._is_color = is_color
        self._stdin_lines = self.get_stdin_lines()

        self._lines = self.get_lines()
        self._colorizer = Colorizer()

    def _get_gpu_usage_and_separator(self) -> List[str]:
        gpu_usage_lines: List[str] = []
        for line in self._lines:
            if not line.startswith(self.PROCESSES_START):
                gpu_usage_lines.append(line)
            else:
                break

        return gpu_usage_lines

    def get_lines(self) -> List[str]:

        fake_stdin = get_fake_stdin()
        if fake_stdin is not None:
            lines = fake_stdin
        elif self._stdin_lines:
            lines = self._stdin_lines
        else:
            processes = subprocess.run(self.COMMAND, stdout=subprocess.PIPE)
            lines_proc = processes.stdout.decode().split("\n")
            lines = [line for line in lines_proc[:-1]]
            lines += lines_proc[-1]

        return lines

    def get_gpu_num_from_line(self, line: List[str]) -> str:
        return line[1]

    def get_pid_from_line(self, line: List[str]) -> str:
        return line[2]

    def get_gpu_mem_from_line(self, line: List[str]) -> str:
        return line[-2]

    def get_stdin_lines(self) -> List[str]:
        if sys.stdin in select.select([sys.stdin], [], [], 0)[0]:
            return sys.stdin.readlines()
        else:
            return []

    def get_line_separator(self) -> str:
        lines = self._get_gpu_usage_and_separator()
        return lines[-1]

    def get_gpu_usage_lines(self) -> List[str]:
        lines = self._get_gpu_usage_and_separator()
        return lines[:-2]

    def get_gpu_processes(self) -> List[GPUProcess]:

        gpu_processes: List[GPUProcess] = []

        for i, line in enumerate(self._lines):
            if line.startswith(self.PROCESSES_START):
                # the process name is displayed after 3 lines
                i += 3
                break

        while not self._lines[i].startswith("+--"):
            if self.NOT_SUPPORTED in line:
                # go on to the next row
                i += 1
                continue

            line = self._lines[i]
            line = self.PATTERN.split(line)

            gpu_num = self.get_gpu_num_from_line(line)
            pid = self.get_pid_from_line(line)
            gpu_mem = self.get_gpu_mem_from_line(line)

            gpu_process = GPUProcess(pid, gpu_num, gpu_mem)
            gpu_processes.append(gpu_process)

            # go on to the next row
            i += 1

        return gpu_processes

    def print_lines(self) -> None:

        gpu_usage_lines = self.get_gpu_usage_lines()
        if self._is_color:
            gpu_usage_lines = self._colorizer.colorize(gpu_usage_lines)

        # ignore last element because it's separator
        gpu_usage_lines = gpu_usage_lines[:-1]

        for line in gpu_usage_lines:
            print(line)
        print(f"{self.get_line_separator()}\n")

        # no running process then exit
        if not self.is_there_running_process():
            self.print_no_running_proces_found()
            sys.exit()

    def print_no_running_proces_found(self) -> None:
        print(self.get_line_separator())
        print(
            "|  "
            + self.NO_RUNNING_PROCESS
            + " " * (73 - len(self.NO_RUNNING_PROCESS))
            + "  |"
        )
        print(self.get_line_separator())

    def is_there_running_process(self) -> bool:
        for i, line in enumerate(self._lines):
            if line.startswith(self.PROCESSES_START):
                # the process name is displayed after 3 lines
                i += 3
                break

        if self.NO_RUNNING_PROCESS in self._lines[i]:
            return False

        return True
