import subprocess

def sh(*args):
    return subprocess.check_output(args)
