import re
import subprocess
from typing import List

from nvhtop.process import CPUProcess


class ProcessStatus(object):
    PS_FORMAT = "pid,user,%cpu,%mem,etime,command"
    PATTERN = re.compile(r"\s+")
    MAX_SPLIT = 5

    def __init__(self, pids: List[int]) -> None:
        self._pids = pids
        self._command = ["ps", "-o", self.PS_FORMAT, "-p", ",".join(pids)]

    def get_pid_from_parts(self, parts: List[str]) -> str:
        return parts[0]

    def get_user_from_parts(self, parts: List[str]) -> str:
        return parts[1]

    def get_cpu_from_parts(self, parts: List[str]) -> str:
        return parts[2]

    def get_mem_from_parts(self, parts: List[str]) -> str:
        return parts[3]

    def get_time_from_parts(self, parts: List[str]) -> str:
        return parts[4] if "-" not in parts[4] else parts[4].split("-")[0] + "days"

    def get_command_from_parts(self, parts: List[str]) -> str:
        return parts[5][0:100]

    def parse_ps_output(self, line: str) -> CPUProcess:

        parts = self.PATTERN.split(line.strip(), self.MAX_SPLIT)
        pid = self.get_pid_from_parts(parts)
        user = self.get_user_from_parts(parts)
        cpu = self.get_cpu_from_parts(parts)
        mem = self.get_mem_from_parts(parts)
        time = self.get_time_from_parts(parts)
        command = self.get_command_from_parts(parts)

        return CPUProcess(pid, user, cpu, mem, time, command)

    def get_cpu_processes(self) -> List[CPUProcess]:

        processes = subprocess.run(self._command, stdout=subprocess.PIPE)
        lines = processes.stdout.decode().strip().split("\n")

        if len(lines) < 2:
            return [CPUProcess(pid) for pid in self._pids]

        cpu_processes: List[CPUProcess] = []
        for line in lines:

            if not (line.strip().startswith("PID") or len(line) == 0):
                cpu_process = self.parse_ps_output(line)
                cpu_processes.append(cpu_process)

        return cpu_processes
