import json
from pathlib import Path

import click

CONFIG_FOLDER = str(Path.home()) + '/.vk-sherlock/'
CONFIG_PATH = CONFIG_FOLDER + 'config.json'


def write_result(path, string):
    with open(path, 'a', encoding='utf-8') as file:
        file.write(json.dumps(string))
        file.write('\n')


def open_result(path):
    user_ids = []

    try:
        with open(path, 'r', encoding='utf-8') as file:
            lines = file.readlines()
            for line in lines:
                user = json.loads(line)
                user_ids.append(user['id'])
    except FileNotFoundError:
        click.echo("File not found")
    except KeyError:
        click.echo("Can't find id")

    return user_ids


def account_info():
    try:
        make_folder()
        with open(CONFIG_PATH, 'r', encoding='utf-8') as file:
            text = ''.join(i for i in file.readlines())

        return list(json.loads(text).keys())[0]

    except FileNotFoundError:
        return False


def print_result(people, write_path):
    for user in people:
        if write_path:
            write_result(write_path, user)
        for k, v in user.items():
            print('{}: {},'.format(k, v), end=' ')
        print('')


def make_folder():
    if not Path.exists(Path(CONFIG_FOLDER)):
        Path.mkdir(Path(CONFIG_FOLDER))
