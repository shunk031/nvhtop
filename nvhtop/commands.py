import argparse
from typing import List

from nvhtop.htop import Htop
from nvhtop.nvidia_smi import NvidiaSmi
from nvhtop.process import CPUProcess, GPUProcess
from nvhtop.ps import ProcessStatus


def create_parser(prog: str = None) -> argparse.ArgumentParser:

    description = (
        "print GPU utilization with usernames "
        "and CPU stats for each GPU-utilizing process"
    )
    parser = argparse.ArgumentParser(description=description)

    cl_help = (
        "Print longer part of the commandline. "
        "If `length' is provided, use it as the commandline length, "
        "otherwise print first 100 characters."
    )
    parser.add_argument(
        "-l",
        "--command-length",
        default=20,
        const=100,
        type=int,
        nargs="?",
        help=cl_help,
    )

    color_help = (
        "Colorize the output (green - free GPU, "
        "yellow - moderately used GPU, red - fully used GPU)"
    )
    parser.add_argument(
        "-c", "--color", action="store_true", help=color_help,
    )
    return parser


def main(prog: str = None) -> None:
    parser = create_parser(prog)
    args = parser.parse_args()

    # for testing, the stdin can be provided in a file
    nvidia_smi = NvidiaSmi(args.color)
    nvidia_smi.print_lines()
    line_separator = nvidia_smi.get_line_separator()

    # get GPU processes
    gpu_processes: List[GPUProcess] = nvidia_smi.get_gpu_processes()
    pids = [process.pid for process in gpu_processes]
    ps = ProcessStatus(pids)

    # get CPU processes
    cpu_processes: List[CPUProcess] = ps.get_cpu_processes()

    htop = Htop(cpu_processes, gpu_processes, line_separator, args.command_length)
    htop.print_lines()
