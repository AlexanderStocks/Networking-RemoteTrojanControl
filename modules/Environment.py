import os


# retrieves environment variables set in target machine
def run(**args):
    print("[*] In environment module.")

    return str(os.environ)