#!/usr/bin/python3
"""Fabric script that generates a .tgz archive from the contents
   of the web_static folder of your AirBnB Clone repo"""

from fabric.api import local
from datetime import datetime
import os


def do_pack():
    """Creates a .tgz archive from the contents of the web_static folder"""

    # Create the versions folder if it doesn't exist
    local("mkdir -p versions")

    # Get the current date and time
    now = datetime.now()
    timestamp = now.strftime("%Y%m%d%H%M%S")

    # Set the archive path
    archive_path = "versions/web_static_{}.tgz".format(timestamp)

    # Create the .tgz archive
    result = local("tar -cvzf {} web_static".format(archive_path))

    # Check if the archive has been correctly generated
    if result.failed:
        return None
    else:
        return archive_path


if __name__ == "__main__":
    do_pack()
