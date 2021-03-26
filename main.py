import platform
import sys

def check_version():
    print("Checking Python version")
    if sys.version_info.major < 3:
        raise AttributeError("Minimum version requires is 3.x")
    print("Python version: {0}.{1} OK".format(sys.version_info.major, sys.version_info.minor))


def check_os():
    print("OS: {0}".format(platform.system()))
    return platform.system() == "Windows"


if __name__  == "__main__":
    #Check Python version and raise an error if < 3.X
    check_version()
    #Check OS to know how to handle system calls
    is_windows = check_os()
