def search_geo_photo(vk, count, lat, long, radius):
    result = vk.photos.search(lat=lat, long=long, radius=radius, count=count)

    return result['count'], result['items']
