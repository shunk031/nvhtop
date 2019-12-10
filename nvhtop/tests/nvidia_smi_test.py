import os

from nvhtop.nvidia_smi import NvidiaSmi
from nvhtop.process import GPUProcess
from nvhtop.tests import NvHtopTestCase


class TestNvidiaSmi(NvHtopTestCase):
    def setUp(self):

        # set environmental variable "FAKE_STDIN_PATH"
        os.environ["FAKE_STDIN_PATH"] = str(self.FIXTURES_ROOT / "fake_stdin.txt")

        self.ns_list = [NvidiaSmi(is_color=True), NvidiaSmi(is_color=False)]

    def test_get_lines(self):

        true_lines_fpath = self.FIXTURES_ROOT / "fake_stdin.txt"
        with true_lines_fpath.open("r") as rf:
            true_lines = [line.strip() for line in rf.readlines()]

        for ns in self.ns_list:

            lines = ns.get_lines()
            assert len(lines) == len(true_lines)
            for line, true_line in zip(lines, true_lines):
                assert line == true_line, f"{line} is not {true_line}"

    # def test_stdin_lines(self):

    #     for ns in self.ns_list:
    #         std_lines = ns.get_stdin_lines()

    def test_get_gpu_num_from_line(self):

        true_line_fpath = self.FIXTURES_ROOT / "gpu_usage_line.txt"
        with true_line_fpath.open("r") as rf:
            true_line = rf.readline().strip()

        for ns in self.ns_list:
            line = ns.PATTERN.split(true_line)
            assert ns.get_gpu_num_from_line(line) == "0"

    def test_get_pid_from_line(self):
        true_line_fpath = self.FIXTURES_ROOT / "gpu_usage_line.txt"
        with true_line_fpath.open("r") as rf:
            true_line = rf.readline().strip()

        for ns in self.ns_list:
            line = ns.PATTERN.split(true_line)
            assert ns.get_pid_from_line(line) == "1032"

    def test_get_gpu_mem_from_line(self):

        true_line_fpath = self.FIXTURES_ROOT / "gpu_usage_line.txt"
        with true_line_fpath.open("r") as rf:
            true_line = rf.readline().strip()

        for ns in self.ns_list:
            line = ns.PATTERN.split(true_line)
            assert ns.get_gpu_mem_from_line(line) == "10781MiB"

    def test_get_line_separator(self):

        true_separator_fpath = self.FIXTURES_ROOT / "line_separator.txt"
        with true_separator_fpath.open("r") as rf:
            true_separator = rf.readline().strip()

        for ns in self.ns_list:
            separator = ns.get_line_separator()
            assert separator == true_separator, f"{separator} is not {true_separator}"

    def test_get_gpu_usage_lines(self):

        true_gpu_usage_lines_fpath = self.FIXTURES_ROOT / "gpu_usage_lines.txt"
        with true_gpu_usage_lines_fpath.open("r") as rf:
            true_lines = [line.strip() for line in rf.readlines()]

        for ns in self.ns_list:
            lines = ns.get_gpu_usage_lines()
            assert len(lines) == len(true_lines)

            for line, true_line in zip(lines, true_lines):
                assert line == true_line

    def test_get_gpu_processes(self):

        true_processes = [
            GPUProcess(pid="1032", gpu_num="0", gpu_mem="10781MiB"),
            GPUProcess(pid="11021", gpu_num="1", gpu_mem="10765MiB"),
            GPUProcess(pid="25544", gpu_num="2", gpu_mem="10775MiB"),
            GPUProcess(pid="4755", gpu_num="3", gpu_mem="389MiB"),
            GPUProcess(pid="14518", gpu_num="3", gpu_mem="7589MiB"),
            GPUProcess(pid="13956", gpu_num="4", gpu_mem="5480MiB"),
            GPUProcess(pid="14293", gpu_num="4", gpu_mem="145MiB"),
            GPUProcess(pid="14294", gpu_num="4", gpu_mem="145MiB"),
            GPUProcess(pid="14295", gpu_num="4", gpu_mem="145MiB"),
            GPUProcess(pid="17547", gpu_num="5", gpu_mem="10765MiB"),
            GPUProcess(pid="11527", gpu_num="6", gpu_mem="10221MiB"),
            GPUProcess(pid="27159", gpu_num="6", gpu_mem="577MiB"),
            GPUProcess(pid="9908", gpu_num="7", gpu_mem="7755MiB"),
        ]

        for ns in self.ns_list:
            processes = ns.get_gpu_processes()
            assert len(processes) == len(true_processes)

            for p1, p2 in zip(processes, true_processes):
                assert isinstance(p1, GPUProcess)
                assert p1 == p2, f"{p1} is not {p2}"

    def test_is_there_running_process(self):

        for ns in self.ns_list:
            cond = ns.is_there_running_process()
            assert cond is True

        os.environ["FAKE_STDIN_PATH"] = str(
            self.FIXTURES_ROOT / "fake_stdin_no_running_process.txt"
        )
        ns_no_process = NvidiaSmi()
        cond = ns_no_process.is_there_running_process()
        assert cond is False
