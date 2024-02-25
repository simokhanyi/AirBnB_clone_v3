#!/usr/bin/python3
"""
Fabric script that deletes out-of-date archives
"""
from fabric.api import local, run, env
from datetime import datetime
from os.path import exists
env.hosts = ['<IP web-01>', '<IP web-02>']


def do_clean(number=0):
    """
    Delete unnecessary archives on both web servers
    """
    try:
        number = int(number)
        if number < 0:
            return False

        # Delete unnecessary archives in the versions folder
        local("ls -t versions | "
              "tail -n +{} | "
              "xargs -I {{}} rm versions/{{}}".format(number + 1))

        # Delete unnecessary archives in /data/web_static/releases on each web
        run("ls -t /data/web_static/releases | tail -n +{} | xargs -I {{}} "
            "rm -rf /data/web_static/releases/{{}}".format(number + 1))
        return True
    except Exception as e:
        return False


if __name__ == "__main__":
    do_clean()
