import os
from typing import List

from nvhtop.nvidia_smi import NvidiaSmi
from nvhtop.process import CPUProcess
from nvhtop.ps import ProcessStatus
from nvhtop.tests import NvHtopTestCase


class TestProcessStatus(NvHtopTestCase):
    def setUp(self):

        # set environmental variable "FAKE_STDIN_PATH"
        os.environ["FAKE_STDIN_PATH"] = str(self.FIXTURES_ROOT / "fake_stdin.txt")
        ns = NvidiaSmi()

        processes = ns.get_gpu_processes()
        self.ps = ProcessStatus([p.pid for p in processes])

    def _load_ps_lines(self) -> List[str]:
        test_ps_lines_fpath = self.FIXTURES_ROOT / "ps_lines.txt"
        with test_ps_lines_fpath.open("r") as rf:
            test_ps_lines = rf.readlines()
        return test_ps_lines

    def test_get_pid_from_parts(self) -> str:
        true_pids = ["3033", "2177", "15980", "13938", "21113", "8560", "5414", "25246"]
        test_ps_lines = self._load_ps_lines()
        assert len(true_pids) == len(test_ps_lines)

        for line, true_pid in zip(test_ps_lines, true_pids):
            parts = self.ps.PATTERN.split(line.strip(), self.ps.MAX_SPLIT)
            assert self.ps.get_pid_from_parts(parts) == true_pid

    def test_get_user_from_parts(self) -> str:
        true_users = [
            "user1",
            "user2",
            "user3",
            "user4",
            "user5",
            "user6",
            "user7",
            "user8",
        ]
        test_ps_lines = self._load_ps_lines()
        assert len(true_users) == len(test_ps_lines)

        for line, true_user in zip(test_ps_lines, true_users):
            parts = self.ps.PATTERN.split(line.strip(), self.ps.MAX_SPLIT)
            assert self.ps.get_user_from_parts(parts) == true_user

    def test_get_cpu_from_parts(self) -> str:
        true_cpus = ["3.7", "92.8", "46.3", "118", "156", "161", "66.5", "1.8"]
        test_ps_lines = self._load_ps_lines()
        assert len(true_cpus) == len(test_ps_lines)

        for line, true_cpu in zip(test_ps_lines, true_cpus):
            parts = self.ps.PATTERN.split(line.strip(), self.ps.MAX_SPLIT)
            assert self.ps.get_cpu_from_parts(parts) == true_cpu

    def test_get_mem_from_parts(self) -> str:
        true_mems = ["4.3", "1.8", "3.1", "5.6", "2.2", "0.8", "0.9", "0.9"]
        test_ps_lines = self._load_ps_lines()
        assert len(true_mems) == len(test_ps_lines)

        for line, true_mem in zip(test_ps_lines, true_mems):
            parts = self.ps.PATTERN.split(line.strip(), self.ps.MAX_SPLIT)
            assert self.ps.get_mem_from_parts(parts) == true_mem

    def test_get_time_from_parts(self) -> str:
        true_times = [
            "2days",
            "53:58",
            "18days",
            "14:48",
            "1days",
            "03:01:17",
            "40:26",
            "03:21:13",
        ]
        test_ps_lines = self._load_ps_lines()
        assert len(true_times) == len(test_ps_lines)

        for line, true_time in zip(test_ps_lines, true_times):
            parts = self.ps.PATTERN.split(line.strip(), self.ps.MAX_SPLIT)
            assert self.ps.get_time_from_parts(parts) == true_time

    def test_get_command_from_parts(self) -> str:
        true_commands = [
            "/usr/local/matlab90/bin/glnxa6",
            "python train_from_predicted.py",
            "python3 src/main.py",
            "python3 resnet16.py --model resnet16",
            "python deep_learing/train.py",
            "python3 train-e2e-shared-layer.py",
            "python voc_2007_classification.py",
            "python3 model_.py --start_epoch 1",
        ]
        test_ps_lines = self._load_ps_lines()
        assert len(true_commands) == len(test_ps_lines)

        for line, true_command in zip(test_ps_lines, true_commands):
            parts = self.ps.PATTERN.split(line.strip(), self.ps.MAX_SPLIT)
            assert self.ps.get_command_from_parts(parts) == true_command

    def test_parse_ps_output(self):

        true_cpu_processes = [
            CPUProcess(
                pid="3033",
                user="user1",
                cpu="3.7",
                mem="4.3",
                time="2days",
                command="/usr/local/matlab90/bin/glnxa6",
            ),
            CPUProcess(
                pid="2177",
                user="user2",
                cpu="92.8",
                mem="1.8",
                time="53:58",
                command="python train_from_predicted.py",
            ),
            CPUProcess(
                pid="15980",
                user="user3",
                cpu="46.3",
                mem="3.1",
                time="18days",
                command="python3 src/main.py",
            ),
            CPUProcess(
                pid="13938",
                user="user4",
                cpu="118",
                mem="5.6",
                time="14:48",
                command="python3 resnet16.py --model resnet16",
            ),
            CPUProcess(
                pid="21113",
                user="user5",
                cpu="156",
                mem="2.2",
                time="1days",
                command="python deep_learing/train.py",
            ),
            CPUProcess(
                pid="8560",
                user="user6",
                cpu="161",
                mem="0.8",
                time="03:01:17",
                command="python3 train-e2e-shared-layer.py",
            ),
            CPUProcess(
                pid="5414",
                user="user7",
                cpu="66.5",
                mem="0.9",
                time="40:26",
                command="python voc_2007_classification.py",
            ),
            CPUProcess(
                pid="25246",
                user="user8",
                cpu="1.8",
                mem="0.9",
                time="03:21:13",
                command="python3 model_.py --start_epoch 1",
            ),
        ]

        test_ps_lines = self._load_ps_lines()
        assert len(true_cpu_processes) == len(test_ps_lines)

        for line, ture_cpu_process in zip(test_ps_lines, true_cpu_processes):
            cpu_process = self.ps.parse_ps_output(line)
            assert (
                cpu_process == ture_cpu_process
            ), f"{cpu_process} is not {ture_cpu_process}"

    def test_get_cpu_processes(self):

        true_processes = [
            CPUProcess(pid="1032"),
            CPUProcess(pid="11021"),
            CPUProcess(pid="25544"),
            CPUProcess(pid="4755"),
            CPUProcess(pid="14518"),
            CPUProcess(pid="13956"),
            CPUProcess(pid="14293"),
            CPUProcess(pid="14294"),
            CPUProcess(pid="14295"),
            CPUProcess(pid="17547"),
            CPUProcess(pid="11527"),
            CPUProcess(pid="27159"),
            CPUProcess(pid="9908"),
        ]

        processes = self.ps.get_cpu_processes()
        assert len(processes) == len(true_processes)

        for p1, p2 in zip(processes, true_processes):
            assert isinstance(p1, CPUProcess)
            assert p1 == p2, f"{p1} is not {p2}"
