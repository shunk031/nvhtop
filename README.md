# nvhtop

![Python 3.7](https://img.shields.io/badge/python-3.7%2B-brightgreen.svg)
[![Actions Status](https://github.com/shunk031/nvhtop/workflows/Python%20package/badge.svg)](https://github.com/shunk031/nvhtop/actions)
![PyPI](https://img.shields.io/pypi/v/nvhtop)

A tool for enriching the output of `nvidia-smi` forked from [peci1/nvidia-htop](https://github.com/peci1/nvidia-htop).

# Install
`pip install .`

## Usage

```
usage: nvhtop [-h] [-l [COMMAND_LENGTH]] [-c]

print GPU utilization with usernames and CPU stats for each GPU-utilizing
process

optional arguments:
  -h, --help            show this help message and exit
  -l [COMMAND_LENGTH], --command-length [COMMAND_LENGTH]
                        Print longer part of the commandline. If `length' is
                        provided, use it as the commandline length, otherwise
                        print first 100 characters.
  -c, --color           Colorize the output (green - free GPU, yellow -
                        moderately used GPU, red - fully used GPU)
```

Note: for backward compatibility, `nvidia-smi | nvhtop [-l [length]]` is also supported.

## Example output

```
$ nvhtop -l

Mon May 21 15:06:35 2018
+-----------------------------------------------------------------------------+
| NVIDIA-SMI 390.25                 Driver Version: 390.25                    |
|-------------------------------+----------------------+----------------------+
| GPU  Name        Persistence-M| Bus-Id        Disp.A | Volatile Uncorr. ECC |
| Fan  Temp  Perf  Pwr:Usage/Cap|         Memory-Usage | GPU-Util  Compute M. |
|===============================+======================+======================|
|   0  GeForce GTX 108...  Off  | 00000000:04:00.0 Off |                  N/A |
| 53%   75C    P2   174W / 250W |  10807MiB / 11178MiB |     97%      Default |
+-------------------------------+----------------------+----------------------+
|   1  GeForce GTX 108...  Off  | 00000000:05:00.0 Off |                  N/A |
| 66%   82C    P2   220W / 250W |  10783MiB / 11178MiB |    100%      Default |
+-------------------------------+----------------------+----------------------+
|   2  GeForce GTX 108...  Off  | 00000000:08:00.0 Off |                  N/A |
| 45%   67C    P2    85W / 250W |  10793MiB / 11178MiB |     51%      Default |
+-------------------------------+----------------------+----------------------+
+-----------------------------------------------------------------------------+
|  GPU   PID     USER    GPU MEM  %MEM  %CPU  COMMAND                         |
|    0  1032 anonymou   10781MiB   308   3.7  python train_classifier.py      |
|    1 11021 cannotte   10765MiB   114   1.5  python3 ./train.py              |
|    2 25544 nevermin   10775MiB   108   2.0  python -m xxxxxxxxxxxxxxxxxxxxx |
+-----------------------------------------------------------------------------+
```

## Screenshot with output coloring

![Screenshot](https://raw.githubusercontent.com/shunk031/nvhtop/master/.github/screen.png)
