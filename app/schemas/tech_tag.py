from pydantic import BaseModel, ConfigDict

class TechTagBase(BaseModel):
    name: str

    model_config = ConfigDict(from_attributes=True)


class TechTagCreate(TechTagBase):
    pass


class TechTagRead(TechTagBase):
    id: int

