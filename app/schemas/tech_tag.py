from pydantic import BaseModel, ConfigDict

class TechTagBase(BaseModel):
    name: str

<<<<<<< HEAD
=======
class TechTagCreate(BaseModel):
    name: str = Field(min_length=1, max_length=100)


class TechTagRead(BaseModel):
>>>>>>> develop
    model_config = ConfigDict(from_attributes=True)


class TechTagCreate(TechTagBase):
    pass


class TechTagRead(TechTagBase):
    id: int

