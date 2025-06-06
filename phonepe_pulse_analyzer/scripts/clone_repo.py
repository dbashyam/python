import os
from git import Repo

REPO_URL = "https://github.com/PhonePe/pulse.git"
LOCAL_PATH = "data/raw_repo"

def clone_repo():
    if os.path.exists(LOCAL_PATH):
        print("Repository already exists.")
        return
    print("Cloning repository...")
    Repo.clone_from(REPO_URL, LOCAL_PATH)
    print("Repository cloned successfully.")
