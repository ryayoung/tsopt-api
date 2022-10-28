# Maintainer:     Ryan Young
# Last Modified:  Oct 08, 2022
from tsopt import Model
from .schema import ModelData, User

# Types
Dimensions = tuple[int, int]
ListVec2D = list[list[float]]

class Session:
    mod: Model = Model()
    user: User|None = None

    @classmethod
    def init_from_user(cls, user: User):
        cls.user = user
        cls.mod = user.model.to_model()

    @classmethod
    def from_model_data(cls, new: ModelData):
        cls.mod = new.to_model()

    @classmethod
    def to_model_data(cls) -> ModelData:
        return ModelData.from_model(cls.mod)

# Variables
# MOD: Model = Model()
# USER: User|None = None
# NAME: str = "New Model"
# 
# 
# def init_from_stored(stored: StoredModel):
    # global MOD, NAME
    # MOD = stored.to_model()
    # NAME = stored.name
# 
# 
# def curr_as_storedmodel() -> StoredModel:
    # global MOD, USER, NAME
    # return StoredModel.from_model(MOD, USER, NAME)


# mod_init_layers: list[str] = []
# mod_init_costs: list[str | Dimensions | ListVec2D ] = []
