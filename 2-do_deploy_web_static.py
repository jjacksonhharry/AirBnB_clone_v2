#!/usr/bin/python3
"""
Fabric script that distributes an archive to your web servers and deploys it.
"""

import os
from fabric.api import env, put, run
from datetime import datetime

env.hosts = ["54.210.96.128", "35.153.79.81"]
env.user = "ubuntu"


def do_pack():
    """
    return the archive path if archive has generated correctly.
    """
    local("mkdir -p versions")
    date = datetime.now().strftime("%Y%m%d%H%M%S")
    archived_f_path = "versions/web_static_{}.tgz".format(date)
    t_gzip_archive = local("tar -cvzf {} web_static".format(archived_f_path))

    if t_gzip_archive.succeeded:
        return archived_f_path
    else:
        return None


def do_deploy(archive_path):
    """
    Distributes an archive to web servers and deploys it.
    """
    if not os.path.exists(archive_path):
        return False

    try:
        # Upload the archive to the /tmp/ directory on the web server
        put(archive_path, "/tmp/")

        # Extract the archive to the /data/web_static/releases/ directory
        archive_filename = os.path.basename(archive_path)
        folder_name = archive_filename.split('.')[0]
        release_path = "/data/web_static/releases/{}/".format(folder_name)
        run("mkdir -p {}".format(release_path))
        run("tar -xzf /tmp/{} -C {}".format(archive_filename, release_path))

        # Remove the uploaded archive
        run("rm /tmp/{}".format(archive_filename))

        # Move contents to the appropriate directory
        run("mv {}web_static/* {}".format(release_path, release_path))

        # Delete the old symbolic link
        run("rm -rf /data/web_static/current")

        # Create a new symbolic link
        run("ln -s {} /data/web_static/current".format(release_path))

        print("New version deployed!")
        return True

    except Exception:
        return False
