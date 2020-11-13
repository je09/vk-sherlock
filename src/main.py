from datetime import datetime

import vk_api
import click

from src.commands import groups_command, people_command, photos_command, search_command, db_command
from .utils import account_info, print_result, open_result
from .utils import CONFIG_PATH


@click.group()
@click.option('-l', '--login', type=str, help='Login of VK account')
@click.option('-p', '--password', type=str, help='Login of VK account')
@click.option('-w', '--write', type=str, default='', help='Write user\'s info to file')
@click.pass_context
def cli(ctx, login: str, password: str, write: str):
    """
    CLI util developed to help finding people on VK.com
    https://github.com/je09/vk-sherlock
    """
    ctx.ensure_object(dict)

    account = account_info()
    if not (login and password) and not account:
        login = click.prompt('Input VK login', type=str)
        password = click.prompt('Input VK password', type=str, hide_input=True)

    if account:
        login = account

    vk_session = vk_api.VkApi(login, password, config_filename=CONFIG_PATH)
    try:
        vk_session.auth()
    except vk_api.exceptions.Captcha:
        click.echo('Captcha needed')

    vk = vk_session.get_api()

    ctx.obj['VK'] = vk
    ctx.obj['WRITE'] = write


@cli.command()
@click.option('--id', 'user_ids', type=str, default='', multiple=True, help='User or users id')
@click.option('--info', type=click.IntRange(1, 3), default='1', help='1 - basic, 2 - medium, 3 - full')
@click.option('-c', '--count', type=click.IntRange(20, 1000), default=20, help='Number of friends to return')
@click.option('-o', '--open', 'path', type=str, default='', help='Use id\'s from previous result')
@click.pass_context
def friends(ctx, user_ids, info, path, count):
    """Get user's friends"""
    vk = ctx.obj['VK']

    if path:
        user_ids = open_result(path)

    count, people = people_command.get_user_friends(vk, count, user_ids, info)
    click.echo("Found %s friends" % count)

    print_result(people, ctx.obj['WRITE'])


@cli.command()
@click.option('--id', 'user_ids', type=str, default='', multiple=True, help='User or users id')
@click.option('-c', '--count', type=click.IntRange(20, 1000), default=20, help='Number of groups to return')
@click.option('-o', '--open', 'path', type=str, default='', help='Use id\'s from previous result')
@click.pass_context
def groups(ctx, user_ids, path, count):
    """Get user's groups"""
    vk = ctx.obj['VK']

    if path:
        user_ids = open_result(path)

    count, found_groups = people_command.get_user_groups(vk, count, user_ids)
    click.echo("Found %s groups" % count)

    for group in found_groups:
        click.echo("Name: %s, link: https://vk.com/club%s" % (group['name'], group['id']))


@cli.command()
@click.option('-c', '--count', type=click.IntRange(20, 1000), default=20, help='Number of photos to return')
@click.option('--lat', type=str, default=30, help='Geographical latitude, in degrees (from -90 to 90)')
@click.option('--long', type=str, default=30, help='Geographical longitude, in degrees (from -180 to 180)')
@click.option('--radius', type=int, default=500, help='Radius of search in meters (works very approximately). '
                                                      'Available values: 10, 100, 800, 6000, 50000')
@click.pass_context
def geotags(ctx, lat, long, radius, count):
    """Get list of photos by geo tags"""
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
@click.option('--info', type=click.IntRange(1, 3), default='1', help='1 - basic, 2 - medium, 3 - full')
@click.option('-c', '--count', type=click.IntRange(20, 1000), default=20, help='Number of groups to return')
@click.pass_context
def group_subscribers(ctx, name, info, count):
    """Get subscribers of a group"""
    vk = ctx.obj['VK']

    count, ids = groups_command.get_community_members(vk, count, name)
    click.echo("Found %s members in %s" % (count, name))
    people = people_command.get_user_info(vk, count, ids, info)
    print_result(people, ctx.obj['WRITE'])


@cli.command()
@click.option('--name', type=str, default='', help='Group name')
@click.option('--info', type=click.IntRange(1, 3), default='1', help='1 - basic, 2 - medium, 3 - full')
@click.option('-c', '--count', type=click.IntRange(20, 1000), default=20, help='Number of user\'s to return')
@click.option('--city', type=str, default='', help='City ID')
@click.option('--country', type=str, default='', help='Country ID')
@click.option('--hometown', type=str, default='', help='Hometown ID')
@click.option('--university', type=str, default='', help='University ID')
@click.option('--sex', type=click.IntRange(0, 2), default=0, help='1 — female, 2 — male, 0 — any (default)')
@click.option('--status', type=click.IntRange(0, 7), default=0, help='1 — Not married, 2 — In a relationship, '
                                                                     '3 — Engaged, 4 — Married, 5 — It\'s complicated, '
                                                                     '6 — Actively searching, 7 — In love')
@click.option('--age_from', type=int, help='Minimum age')
@click.option('--age_to', type=int, help='Maximum age')
@click.option('--birth_day', type=str, help='Day of birth')
@click.option('--birth_month', type=str, help='Month of birth')
@click.option('--birth_year', type=str, help='Year of birth')
@click.option('--work', type=str, default='', help='Name of the company where users work')
@click.option('--religion', type=str, default='', help='User\'s religious affiliation')
@click.option('--has_photo', is_flag=True, help='Show users with photo only')
@click.option('--online', is_flag=True, help='Show online users only')
@click.pass_context
def search(ctx, name, work, info, count, city, country, hometown,
           university, sex, status, age_from, age_to, birth_day,
           birth_month, birth_year, religion, online, has_photo):
    """Search for user by provided criteria"""
    vk = ctx.obj['VK']

    count, people = search_command.search(vk, count, name, work, city, country, hometown,
                                          university, sex, status, age_from, age_to, birth_day,
                                          birth_month, birth_year, religion, online, has_photo)
    click.echo('Found %s people' % count)
    ids = [i['id'] for i in people]

    people = people_command.get_user_info(vk, count, ids, info)
    print_result(people, ctx.obj['WRITE'])


@cli.command()
@click.option('--id', 'user_ids', type=str, default='', multiple=True, help='User or users id')
@click.option('--info', type=click.IntRange(1, 3), default='1', help='1 - basic, 2 - medium, 3 - full')
@click.option('-o', '--open', 'path', type=str, default='', help='Use id\'s from previous result')
@click.option('-c', '--count', type=click.IntRange(20, 1000), default=20, help='Number of user\'s to return')
@click.pass_context
def user_info(ctx, user_ids, info, path, count):
    """Get user's profile info"""
    vk = ctx.obj['VK']

    if path:
        user_ids = open_result(path)

    people = people_command.get_user_info(vk, count, user_ids, info)
    print_result(people, ctx.obj['WRITE'])


@cli.command()
@click.option('--country', type=str, default='', help='Country code in ISO 3166-1 alpha-2 standard')
@click.option('--city', type=str, default='', help='City name')
@click.option('--university', type=str, default='', help='University name')
@click.option('--school', type=str, default='', help='School name')
@click.option('-c', '--count', type=click.IntRange(20, 1000), default=20, help='Number of user\'s to return')
@click.pass_context
def db(ctx, count, country, city, university, school):
    """Get id's of objects for searching from VK db"""
    vk = ctx.obj['VK']

    if country:
        c, result = db_command.get_country_id(vk, count, country)
        click.echo('Found %s countries' % c)
        print_result(result, False)

    if city:
        country_code = click.prompt('Input country code in ISO 3166-1 alpha-2 standard')
        _, code = db_command.get_country_id(vk, 1, country_code)
        c, result = db_command.get_city_id(vk, count, code[-1]['id'], city)
        click.echo('Found %s cities' % c)
        print_result(result, False)
        del code, country_code

    if university:
        c, result = db_command.get_university_id(vk, count, university)
        click.echo('Found %s universities' % c)
        print_result(result, False)

    if school:
        country_name = click.prompt('Input country code in ISO 3166-1 alpha-2 standard')
        city_name = click.prompt('Input city name')
        _, country_code = db_command.get_country_id(vk, 1, country_name)
        _, city_code = db_command.get_city_id(vk, count, country_code[0]['id'], city_name)
        c, result = db_command.get_school_id(vk, count, city_code[0]['id'], school)
        click.echo('Found %s schools' % c)
        print_result(result, False)
        del country_name, city_name, country_code, city_code


if __name__ == '__main__':
    cli()
