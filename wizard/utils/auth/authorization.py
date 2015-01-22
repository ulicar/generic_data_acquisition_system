__author__ = 'jdomsic'

def authorize(username, required_roles, db):
    user_roles = get_roles_for_user(username, db)
    for role in required_roles:
        if role not in user_roles:
            return False

    return True

def get_roles_for_user(username, db):
    return ['CORE']