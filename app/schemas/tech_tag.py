from pydantic import BaseModel, ConfigDict, Field, field_validator


class TechTagCreate(BaseModel):
    name: str = Field(min_length=1, max_length=100)

    @field_validator("name")
    @classmethod
    def normalize_name(cls, value: str) -> str:
        normalized = value.strip().lower()
        if not normalized:
            raise ValueError("Tag name must not be blank")
        if "," in normalized:
            raise ValueError("Tag name must not contain a comma")
        return normalized


class TechTagRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str