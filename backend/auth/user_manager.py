import os
import json
from typing import Dict, Any, List

DATA_DIR = "user_data"

class UserManager:
    def __init__(self):
        if not os.path.exists(DATA_DIR):
            os.makedirs(DATA_DIR)

    def _get_user_dir(self, uid: str) -> str:
        user_dir = os.path.join(DATA_DIR, uid)
        if not os.path.exists(user_dir):
            os.makedirs(user_dir)
        return user_dir

    def save_github_token(self, uid: str, token: str):
        # In a real app, encrypt this! using simple file for prototype
        user_dir = self._get_user_dir(uid)
        with open(os.path.join(user_dir, "github_token.txt"), "w") as f:
            f.write(token)

    def get_github_token(self, uid: str) -> str:
        user_dir = self._get_user_dir(uid)
        token_path = os.path.join(user_dir, "github_token.txt")
        if os.path.exists(token_path):
            with open(token_path, "r") as f:
                return f.read().strip()
        return None

user_manager = UserManager()
