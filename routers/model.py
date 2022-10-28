# Maintainer:     Ryan Young
# Last Modified:  Oct 09, 2022
from fastapi import APIRouter
from redis_om import Migrator
from ..schema import (
    ModelData,
)
from ..session import Session

r = APIRouter()
Migrator().run()


@r.get('/')
def get_model():
    return ModelData.from_model(Session.mod)


@r.put('/')
def set_model(model_data: ModelData = ModelData.default_template()):
    Session.mod = model_data.to_model()
