#!/usr/bin/env python3

import os
from secrets import token_urlsafe
from typing import Dict

from dotenv import find_dotenv, load_dotenv, set_key


class Color:
    BLUE = "\033[94m"
    YELLOW = "\033[93m"
    RED = "\033[91m"
    BOLD = "\033[1m"
    RESET = "\033[0m"


def get_postgres_keys() -> Dict[str, str]:
    keys = {
        "POSTGRES_USER": "postgres",
        "POSTGRES_PASSWORD": token_urlsafe(32),
        "POSTGRES_SERVER": "db",
        "POSTGRES_DB": "app",
    }
    print(f"{Color.BLUE}[•] Setting postgres variables.{Color.RESET}")
    for key in keys:
        value = input(f"{Color.BLUE}[>] {key} {Color.BOLD}({keys[key]}){Color.RESET} ")
        if value:
            keys[key] = value
    return keys


def create_env_file() -> bool:
    if os.path.isfile(".env"):
        print(f"{Color.YELLOW}[•] An .env file already exists.{Color.RESET}")
        overwrite = input(
            f"{Color.YELLOW}[>] Do you want to overwrite it? {Color.BOLD}[N/y] {Color.RESET}"
        )
        if overwrite.lower() == "y":
            with open(".env", "w") as env:
                env.truncate()
            return True
        return False
    else:
        print(f"{Color.BLUE}[•] Creating .env file.{Color.RESET}")
        with open(".env", "w"):
            ...
        return True


def config_env_file(keys) -> None:
    dotenv_file = find_dotenv()
    load_dotenv(dotenv_file)
    for key in keys:
        set_key(dotenv_file, key, keys[key])


def main() -> None:
    keys = {**get_postgres_keys(), "FLASK_APP": "app.run.py"}
    created = create_env_file()
    if created:
        config_env_file(keys)
        print(f"{Color.BLUE}[•] .env file successfully created.{Color.RESET}")
    else:
        print(f"{Color.YELLOW}[•] Operation aborted.{Color.RESET}")


if __name__ == "__main__":
    print("[•] ToDoApp.")
    try:
        main()
    except (KeyboardInterrupt, EOFError):
        print(f"\n{Color.RED}[✗] Exiting...{Color.RESET}")
        exit(0)
