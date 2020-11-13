def search(vk, count, name, work, city, country, hometown,
           university, sex, status, age_from, age_to, birth_day, birth_month, birth_year,
           religion, online, has_photo):
    result = vk.users.search(q=name, company=work, count=count, city=city, country=country,
                             hometown=hometown, university=university, sex=sex, status=status,
                             age_from=age_from, age_to=age_to, birth_day=birth_day,
                             birth_mpnth=birth_month, birth_year=birth_year, religion=religion,
                             online=online, has_photo=has_photo)

    return result['count'], result['items']
