from pydantic import BaseModel, Field


class HostBase(BaseModel):
    label: str
    url: str


class HostSchema(HostBase):
    idhost: int

    class Config():
        from_attributes = True


class HostCreateSchema(HostBase):
    ...
