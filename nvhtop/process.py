from dataclasses import dataclass


@dataclass
class Process(object):
    pid: int


@dataclass
class CPUProcess(Process):
    user: str = ""
    cpu: str = ""
    mem: str = ""
    time: str = ""
    command: str = ""


@dataclass
class GPUProcess(Process):
    gpu_num: str
    gpu_mem: str
