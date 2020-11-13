def get_community_members(vk, count, group_id: str):
    result = vk.groups.getMembers(group_id=group_id, count=count)
    return result['count'], result['items']
