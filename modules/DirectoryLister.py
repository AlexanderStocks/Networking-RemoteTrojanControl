import os

# lists all files in current directory
def run(**args):
    print("[*] In DirectoryLister module.")
    files = os.listdir(".")

    return str(files)
