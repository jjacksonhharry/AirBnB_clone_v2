#!/usr/bin/python3
"""
Fabric script that deletes out-of-date archives.
"""

from fabric.api import *
import os

env.hosts = ["54.210.96.128", "35.153.79.81"]
env.user = "ubuntu"


def do_clean(number=0):
    """
    Deletes out-of-date archives.
    """
    try:
        number = int(number)
        if number < 0:
            return False

        number = 1 if number == 0 else number + 1

        # Clean local archives in versions folder
        with lcd("versions"):
            local("ls -t | tail -n +{} | xargs -I {{}} rm {{}}".format(number))

        # Clean remote archives in /data/web_static/releases folder
        with cd("/data/web_static/releases"):
            run("ls -t | tail -n +{} | xargs -I {{}} rm -rf {{}}"
                .format(number))

        print("Cleaned archives successfully!")
        return True

    except Exception:
        return False
