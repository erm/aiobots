def get_url(request, name, kwargs={}, is_ws=False):
    resource = request.app.router[name]
    try:
        resource_path = resource.url_for(**kwargs) if kwargs else resource.url_for()
    except KeyError as e:
        # raise AppRouteURLKeyError(e)
        raise
    settings = request.app['AIOBOTS']['SETTINGS']
    p = 'http://' if not is_ws else 'ws://'
    url = '{}{}:{}{}'.format(p, settings.HOSTNAME, settings.PORT, resource_path)
    return url


def get_reverse_match(match_info):
    return match_info._route._resource._formatter

