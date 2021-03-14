import os
import shutil
from os import path
import urllib3
import subprocess


class RepoClone:
    """
    Class to clone repos from github
    """

    def __init__(self, url, username, access_token, repo_name):
        """
        Initializing the instance
        :param url: url of the desired repo must be HTTPS not SSH
        """
        BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.url = url
        self.username = username
        self.access_token = access_token
        self.repo_name = repo_name
        self.path = str(BASE_DIR + '/temp')

    def __check_path__(self):
        if path.exists(self.path):
            shutil.rmtree(self.path)
        else:
            os.mkdir(self.path)

    def clone(self):
        """
        :return: if the clone is success returns true otherwise false
        """
        self.__check_path__()
        url_check = urllib3.connection_from_url(self.url)
        # checking if the host is github or not
        if url_check.host == 'github.com':
            try:
                __CLONE_URL__ = "https://" + self.username + ":" + self.access_token + "@github.com/" + self.username + "/" + self.repo_name + ".git"
                # giving the cloning process only 15 second as it only downloads single file over the network
                var = subprocess.run(["git", "clone", __CLONE_URL__, self.path], check=True,
                                     stdout=subprocess.PIPE,
                                     timeout=15).stdout
                return True
            except (subprocess.CalledProcessError, subprocess.TimeoutExpired, Exception) as e:
                return False
        else:
            return False
