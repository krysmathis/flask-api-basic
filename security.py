from werkzeug.security import safe_str_cmp
from models.user import UserModel as User


def authenticate(username, password) : 
    """ Authenticate that the given username and password resolve to 
        and active user """
    user = User.find_by_username(username)
    if user and safe_str_cmp(user.password, password) : 
        return user


def identity(payload) : 
    """ the user passes in the user id token"""
    user_id = payload['identity']
    return User.find_by_id(user_id)

