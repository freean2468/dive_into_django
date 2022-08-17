AUTH_TIMEOUT = 300
SIGNUP_TIMEOUT = 900
PASSWORD_TIMEOUT = 300

def make_key_for_signup_auth(key):
    return 'sa_%s' % key


def make_key_for_signup(key):
    return 's_%s' % key


def make_key_for_password_auth(key):
    return 'pa_%s' % key


def make_key_for_password(key):
    return 'p_%s' % key