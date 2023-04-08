import logging

logging.basicConfig(level=logging.DEBUG)


def run():
    _LOGGER = logging.getLogger(__name__)

    import api as fgapi
    username = ''
    password = ''
    dsn = ''
    _LOGGER.debug(f"Added Fujitsu Account for username: {username}")

    api = fgapi.Api(username, password, 'eu')
    if not api._authenticate():
        _LOGGER.error("Unable to authenticate with Fujistsu General")
        return

    from SplitAC import SplitAC
    ac = SplitAC(dsn, api)

    ac.turn_off()




run()
