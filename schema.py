# Maintainer:     Ryan Young
# Last Modified:  Oct 08, 2022
from pydantic import BaseModel, validator
import pandas as pd, numpy as np
from tsopt import Model, NetworkValues
from redis_om import JsonModel, Field
from .db import redis
from .util import hash_to_int


class JsonDF(BaseModel):
    vals: list[list[float|None]] = [[]]
    idxs: list[str] = []
    cols: list[str] = []

    def to_df(self):
        return pd.DataFrame(vals, index=idxs, columns=cols)

    @classmethod
    def from_df(cls, df):
        return cls(
            vals = df.replace({np.nan:None}).values.tolist(),
            idxs = list(df.index),
            cols = list(df.columns)
        )


class JsonDFList(list):

    def to_dfs(self):
        return [df.to_df() for df in self]

    @classmethod
    def from_dfs(cls, dfs):
        return cls([JsonDF.from_df(df) for df in dfs])


class JsonSR(BaseModel):
    vals: list[float|None] = []
    idxs: list[str] = []

    def to_sr(self):
        return pd.Series(vals, index=idxs)

    @classmethod
    def from_sr(cls, sr):
        return cls(
            vals = list(sr.replace({np.nan:None})),
            idxs = list(sr.index),
        )

class JsonSRList(list):

    def to_srs(self):
        return [sr.to_sr() for sr in self]

    @classmethod
    def from_srs(cls, srs):
        return cls([JsonSR.from_sr(sr) for sr in srs])


class JsonNodeConstraints(BaseModel):
    dem: JsonSRList = JsonSRList()
    cap: JsonSRList = JsonSRList()

    @classmethod
    def from_container(cls, container):
        return cls(
            dem = JsonSRList.from_srs(container.dem),
            cap = JsonSRList.from_srs(container.cap),
        )

class JsonEdgeConstraints(BaseModel):
    dem: JsonDFList = JsonDFList()
    cap: JsonDFList = JsonDFList()

    @classmethod
    def from_container(cls, container):
        return cls(
            dem = JsonDFList.from_dfs(container.dem),
            cap = JsonDFList.from_dfs(container.cap),
        )


class JsonConstraints(BaseModel):
    net: NetworkValues = NetworkValues(None, None)
    node: JsonNodeConstraints = JsonNodeConstraints()
    edge: JsonEdgeConstraints = JsonNodeConstraints()

    @classmethod
    def from_container(cls, container):
        return cls(
            net = container.net,
            node = JsonNodeConstraints.from_container(container.node),
            edge = JsonEdgeConstraints.from_container(container.edge),
        )


class ModelData(BaseModel):
    name:           str
    layers:         list[str]
    shape:          list[int]
    costs:          JsonDFList
    con:            JsonConstraints
    units:          str|None

    def to_model(self):
        mod = Model(self.layers, self.shape)
        mod.name = self.name

        for i, df in enumerate(self.costs.to_dfs()):
            mod.costs[i] = df

        # CONSTRAINTS
        # Network
        mod.net.dem = self.con.net.dem
        mod.net.cap = self.con.net.cap

        # Node
        mod.node.dem = self.con.node.dem.to_srs()
        mod.node.cap = self.con.node.cap.to_srs()

        # Edge
        mod.edge.dem = self.con.edge.dem.to_dfs()
        mod.edge.cap = self.con.edge.cap.to_dfs()

        return mod


    @classmethod
    def from_model(cls, model):
        return cls(
            name = model.name,
            layers = model.layers,
            shape = model.shape,
            costs = JsonDFList.from_dfs(model.costs),
            con = JsonConstraints.from_container(model.con),
            units = model.units
        )

    @classmethod
    def default_template(cls):
        mod = Model(['Distributor', 'Retailer'], [2,2])
        return cls.from_model(mod)


class User(JsonModel):
    username: str = Field(index=True)
    pass_hash: int
    model: ModelData = ModelData.default_template()

    class Meta:
        database = redis
