# Maintainer:     Ryan Young
# Last Modified:  Oct 08, 2022
import json
from fastapi import APIRouter, Response
from ..schema import User, ModelData
from ..session import Session
from ..util import hash_to_int

r = APIRouter()

@r.get('/{username}')
async def signin(username: str, password: str):
    pass_hash = hash_to_int(password)
    user = User.get(username)
    if pass_hash == user.pass_hash:
        Session.init_from_user(user)
        return user


@r.get('/{username}/exists/')
async def check_username(username: str):
    if username in User.all_pks():
        return True
    return False


@r.post('/{username}', status_code=201)
async def create(username: str, password: str, response: Response):
    pass_hash = hash_to_int(password)
    if username in User.all_pks():
        existing = User.get(username)
        existing.pass_hash = pass_hash
        response.status_code = 200
        return existing.save()
    new = User(username=username, pass_hash=pass_hash)
    new.pk = username
    return new.save()


@r.put('/model/')
async def update_model(model: ModelData):
    if Session.user:
        Session.user.model = model
        return Session.user.save()
    else:
        raise ValueError("No user signed in")














@r.get("/")
async def all_users():
    return [User.get(pk) for pk in User.all_pks()]


@r.delete('/{username}')
async def delete(username: str):
    return User.delete(username)


