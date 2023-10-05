#!/usr/bin/python3
"""
Fabric script that creates and distributes an archive to web servers.
"""

from fabric.api import *
from os.path import exists
from datetime import datetime
import os

env.hosts = ["54.210.96.128", "35.153.79.81"]
env.user = "ubuntu"


def do_pack():
    """
    Compresses the web_static folder into a .tgz archive.
    """
    try:
        local("mkdir -p versions")
        date = datetime.now().strftime("%Y%m%d%H%M%S")
        archive_path = "versions/web_static_{}.tgz".format(date)
        local("tar -czvf {} web_static".format(archive_path))
        return archive_path
    except Exception:
        return None


def do_deploy(archive_path):
    """
    Distributes an archive to web servers and deploys it.
    """
    if not archive_path or not exists(archive_path):
        return False

    try:
        # Upload the archive to the server
        put(archive_path, "/tmp/")

        # Extract the archive to the new version folder
        archive_filename = os.path.basename(archive_path)
        folder_name = archive_filename.split('.')[0]
        release_path = "/data/web_static/releases/{}/".format(folder_name)
        run("mkdir -p {}".format(release_path))
        run("tar -xzf /tmp/{} -C {}".format(archive_filename, release_path))

        # Remove the uploaded archive
        run("rm /tmp/{}".format(archive_filename))

        # Move contents to the appropriate directory
        run("mv {}web_static/* {}".format(release_path, release_path))

        # Remove the old symbolic link
        run("rm -rf /data/web_static/current")

        # Create a new symbolic link
        run("ln -s {} /data/web_static/current".format(release_path))

        print("New version deployed!")
        return True
    except Exception:
        return False


def deploy():
    """
    Full deployment process: pack and deploy the archive.
    """
    archive_path = do_pack()
    if not archive_path:
        return False
    return do_deploy(archive_path)
