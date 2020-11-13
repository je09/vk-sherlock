def get_country_id(vk, count, country):
    result = vk.database.getCountries(count=count, code=country)
    return result['count'], result['items']


def get_city_id(vk, count, country, city):
    result = vk.database.getCities(count=count, country_id=country, q=city)
    return result['count'], result['items']


def get_university_id(vk, count, university):
    result = vk.database.getUniversities(count=count, q=university)
    return result['count'], result['items']


def get_school_id(vk, count, city, school):
    result = vk.database.getSchools(count=count, city_id=city, q=school)
    return result['count'], result['items']
