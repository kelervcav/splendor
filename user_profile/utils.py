import datetime


def unique_id_generator(id) -> str:
    app = "USER"
    date = datetime.datetime.now().strftime("%Y%m%d")
    id_format = '{:07}'.format(id)

    unique_id = f'{app}-{date}-{id_format}'

    return unique_id
