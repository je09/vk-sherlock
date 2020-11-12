# Info about user
import vk_api
import click

def _id_join(ids: dict):
    return ','.join(str(i) for i in ids)


def get_user_info(vk, count, user_ids: dict, info: int):
    basic_fields = 'uid,first_name,last_name,sex,bdate,city,country,schools,relation,'
    medium_fields = basic_fields + 'home_town,contacts,education,universities,occupation,relatives,connections,exports'
    full_fields = medium_fields + 'verified,online,domain,site,status,last_seen,counters,nickname,personal' \
                                  'activities,interests,music,movies,tv,books,games,about,quotes,'

    fields = basic_fields
    if info == 2:
        fields = medium_fields
    if info == 3:
        fields = full_fields

    result = vk.users.get(user_ids=_id_join(user_ids), count=count, fields=fields)

    return result


def get_user_friends(vk, count, user_ids: dict, info):
    basic_fields = 'uid,first_name,last_name,sex,bdate,city,country,schools,relation,'
    medium_fields = basic_fields + 'home_town,contacts,education,universities,occupation,relatives,connections,exports'
    full_fields = medium_fields + 'verified,online,domain,site,status,last_seen,counters,nickname,personal' \
                                  'activities,interests,music,movies,tv,books,games,about,quotes,'

    fields = basic_fields
    if info == 2:
        fields = medium_fields
    if info == 3:
        fields = full_fields

    result = {'count': 0, 'items': []}
    for user_id in user_ids:
        try:
            friends = vk.friends.get(user_id=user_id, count=count, fields=fields)
            result['count'] += friends['count']
            result['items'].extend(friends['items'])
        except vk_api.exceptions.ApiError:
            click.echo("%i is private, can't get friend list" % user_id)

    return result['count'], result['items']


def get_user_groups(vk, count, user_ids: dict):
    result = {'count': 0, 'items': []}
    for user_id in user_ids:
        groups = vk.freinds.get(user_id=user_id, count=count, extended=1)
        result['count'] += groups['count']
        result['items'].extend(groups['items'])

    return result['count'], result['items']

