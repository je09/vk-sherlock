import json
from datetime import datetime

import vk_api
import click

from src.commands import groups_command, people_command, photos_command, search_command


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
        with open('vk_config.v2.json', 'r', encoding='utf-8') as file:
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


@click.group()
@click.option('-l', '--login', type=str, help='Login of VK account')
@click.option('-p', '--password', type=str, help='Login of VK account')
@click.option('-w', '--write', type=str, default='', help='Write input to file')
@click.pass_context
def cli(ctx, login: str, password: str, write: str):
    ctx.ensure_object(dict)

    account = account_info()
    if not (login and password) and not account:
        login = click.prompt('Input VK login', type=str)
        password = click.prompt('Input VK password', type=str, hide_input=True)

    if account:
        login = account

    vk_session = vk_api.VkApi(login, password)
    try:
        vk_session.auth()
    except vk_api.exceptions.Captcha:
        click.echo('Captcha needed')

    vk = vk_session.get_api()

    ctx.obj['VK'] = vk
    ctx.obj['WRITE'] = write


@cli.command()
@click.option('--id', 'user_ids', type=str, default='', multiple=True, help='User or users id')
@click.option('--info', type=click.IntRange(1, 3), default='1')
@click.option('-c', '--count', type=click.IntRange(20, 1000), default=20)
@click.option('-o', '--open', 'path', type=str, default='', help='Open previous results')
@click.pass_context
def friends(ctx, user_ids, info, path, count):
    vk = ctx.obj['VK']

    if path:
        user_ids = open_result(path)

    count, people = people_command.get_user_friends(vk, count, user_ids, info)
    click.echo("Found %s friends" % count)

    print_result(people, ctx.obj['WRITE'])


@cli.command()
@click.option('--id', 'user_ids', type=str, default='', multiple=True, help='User or users id')
@click.option('-c', '--count', type=click.IntRange(20, 1000), default=20)
@click.option('-o', '--open', 'path', type=str, default='', help='Open previous results')
@click.pass_context
def groups(ctx, user_ids, path, count):
    vk = ctx.obj['VK']

    if path:
        user_ids = open_result(path)

    count, found_groups = people_command.get_user_groups(vk, count, user_ids)
    click.echo("Found %s groups" % count)

    for group in found_groups:
        click.echo("Name: %s, link: https://vk.com/id%s" % (group['name'], group['id']))


@cli.command()
@click.option('-c', '--count', type=click.IntRange(20, 1000), default=20)
@click.option('--lat', type=str, default=30)
@click.option('--long', type=str, default=30)
@click.option('--radius', type=int, default=500)
@click.pass_context
def geo_tags(ctx, lat, long, radius, count):
    vk = ctx.obj['VK']

    photos = photos_command.search_geo_photo(vk, count, lat, long, radius)
    click.echo("Found %s photos" % count)

    for photo in photos[1]:
        click.echo("Date: %s, owner: %i, album id: %i, coordinates: %s %s, link: %s" % (
            datetime.utcfromtimestamp(photo['date']).strftime('%Y-%m-%d'),
            photo['owner_id'],
            photo['album_id'],
            photo['lat'],
            photo['long'],
            photo['sizes'][-1]['url']
        ))


@cli.command()
@click.option('--name', type=str, help='Group name')
@click.option('--info', type=click.IntRange(1, 3), default='1')
@click.option('-c', '--count', type=click.IntRange(20, 1000), default=20)
@click.pass_context
def group_subscribers(ctx, name, info, count):
    vk = ctx.obj['VK']

    count, ids = groups_command.get_community_members(vk, count, name)
    click.echo("Found %s members in %s" % (count, name))
    people = people_command.get_user_info(vk, count, ids, info)
    print_result(people, ctx.obj['WRITE'])


@cli.command()
@click.option('--name', type=str, default='', help='Group name')
@click.option('--info', type=click.IntRange(1, 3), default='1')
@click.option('-c', '--count', type=click.IntRange(20, 1000), default=20)
@click.option('--city', type=str, default='', help='City ID')
@click.option('--country', type=str, default='', help='Country ID')
@click.option('--hometown', type=str, default='', help='Hometown ID')
@click.option('--university', type=str, default='', help='University ID')
@click.option('--sex', type=click.IntRange(0, 2), default=0, help='1 — female, 2 — male, 0 — any (default)')
@click.option('--status', type=click.IntRange(0, 7), default=0, help='1 — Not married, 2 — In a relationship, '
                                                                     '3 — Engaged, 4 — Married, 5 — It\'s complicated, '
                                                                     '6 — Actively searching, 7 — In love')
@click.option('--age_from', type=int)
@click.option('--age_to', type=int)
@click.option('--birth_day', type=str)
@click.option('--birth_month', type=str)
@click.option('--birth_year', type=str)
@click.option('--work', type=str, default='', help='Work name')
@click.pass_context
def search(ctx, name, work, info, count, city, country, hometown,
           university, sex, status, age_from, age_to, birth_day,
           birth_month, birth_year):
    vk = ctx.obj['VK']

    count, people = search_command.search(vk, count, name, work, city, country, hometown,
                                          university, sex, status, age_from, age_to, birth_day,
                                          birth_month, birth_year)
    click.echo('Found %s people' % count)
    ids = [i['id'] for i in people]

    people = people_command.get_user_info(vk, count, ids, info)
    print_result(people, ctx.obj['WRITE'])


@cli.command()
@click.option('--id', 'user_ids', type=str, default='', multiple=True, help='User or users id')
@click.option('--info', type=click.IntRange(1, 3), default='1')
@click.option('-o', '--open', 'path', type=str, default='', help='Open previous results')
@click.pass_context
def user_info(ctx, user_ids, info, path):
    vk = ctx.obj['VK']

    if path:
        user_ids = open_result(path)

    people = people_command.get_user_info(vk, user_ids, info)
    print_result(people, ctx.obj['WRITE'])


if __name__ == '__main__':
    cli()
