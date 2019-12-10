import os

from nvhtop.htop import Htop
from nvhtop.nvidia_smi import NvidiaSmi
from nvhtop.ps import ProcessStatus
from nvhtop.tests import NvHtopTestCase


class TestHtop(NvHtopTestCase):
    def setUp(self):

        # set environmental variable "FAKE_STDIN_PATH"
        os.environ["FAKE_STDIN_PATH"] = str(self.FIXTURES_ROOT / "fake_stdin.txt")

        ns = NvidiaSmi()
        line_separator = ns.get_line_separator()
        gpu_processes = ns.get_gpu_processes()

        pids = [process.pid for process in gpu_processes]
        ps = ProcessStatus(pids)
        cpu_processes = ps.get_cpu_processes()

        self.htop = Htop(cpu_processes, gpu_processes, line_separator)

    def test_get_htop_lines(self):

        true_htop_lines_fpath = self.FIXTURES_ROOT / "htop_lines.txt"
        with true_htop_lines_fpath.open("r") as rf:
            true_htop_lines = [line.strip() for line in rf.readlines()]

        lines = self.htop.get_htop_lines()
        assert len(lines) == len(true_htop_lines)

        for line, true_line in zip(lines, true_htop_lines):
            assert line == true_line
