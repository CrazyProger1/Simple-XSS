import subprocess

from typeguard import typechecked


@typechecked
def execute(command: str, shell: bool = False) -> subprocess.Popen:
    return subprocess.Popen(
        command,
        stderr=subprocess.PIPE,
        stdout=subprocess.PIPE,
        shell=shell
    )
