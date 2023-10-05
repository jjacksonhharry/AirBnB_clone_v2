#!/usr/bin/python3
"""
Fabric script that generates a .tgz archive from
the contents of the web_static folder
"""

from fabric.api import local
from datetime import datetime


def do_pack():
    """
    Compresses the web_static folder contents into a .tgz archive.
    """
    try:
        # Create the 'versions' directory if it doesn't exist
        local("mkdir -p versions")

        # Generate the timestamp for the archive filename
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")

        # Create the archive file using tar
        archive_filename = "versions/web_static_{}.tgz".format(timestamp)
        local("tar -cvzf {} web_static".format(archive_filename))

        return archive_filename

    except Exception:
        return None
