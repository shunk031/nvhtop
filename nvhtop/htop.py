from typing import List

from nvhtop.process import CPUProcess, GPUProcess


class Htop(object):
    def __init__(
        self,
        cpu_processes: List[CPUProcess],
        gpu_processes: List[GPUProcess],
        line_separator: str,
        command_length: int = 20,
    ) -> None:

        self._line_separator = line_separator
        self._command_length = command_length
        self._cpu_processes = sorted(cpu_processes, key=lambda x: x.pid)
        self._gpu_processes = sorted(gpu_processes, key=lambda x: x.pid)

        self._template = (
            "|  %3s %5s %8s   %8s %5s %5s %9s  %-"
            + str(command_length)
            + "."
            + str(command_length)
            + "s  |"
        )

    def get_header_line(self) -> str:
        header = self._template % (
            "GPU",
            "PID",
            "USER",
            "GPU MEM",
            "%CPU",
            "%MEM",
            "TIME",
            "COMMAND",
        )
        return header

    def get_process_lines(self) -> List[str]:
        cpu_pids = list(map(lambda x: x.pid, self._cpu_processes))

        lines = []
        for g in self._gpu_processes:
            c = self._cpu_processes[cpu_pids.index(g.pid)]
            lines.append(
                self._template
                % (g.gpu_num, c.pid, c.user, g.gpu_mem, c.cpu, c.mem, c.time, c.command)
            )
        return lines

    def get_htop_lines(self) -> List[str]:

        lines = [self._line_separator]
        lines.append(self.get_header_line())
        lines.extend(self.get_process_lines())
        lines.append(self._line_separator)

        return lines

    def print_lines(self) -> None:

        lines = self.get_htop_lines()
        for line in lines:
            print(line)

        # print(self._line_separator)
        # print(
        #     self._template
        #     % ("GPU", "PID", "USER", "GPU MEM", "%CPU", "%MEM", "TIME", "COMMAND")
        # )
        # print(self._line_separator)

        # cpu_pids = list(map(lambda x: x.pid, self._cpu_processes))
        # for g in self._gpu_processes:
        #     c = self._cpu_processes[cpu_pids.index(g.pid)]
        #     print(
        #         self._template
        #         % (g.gpu_num, c.pid, c.user, g.gpu_mem, c.cpu, c.mem, c.time, c.command)
        #     )

        # print(self._line_separator)
