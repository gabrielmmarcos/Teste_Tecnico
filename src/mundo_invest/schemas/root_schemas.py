from pydantic import BaseModel, Field


# schemas padrao de menssagem
class Message(BaseModel):
    message: str


# schemas para filter nos endpoint get
class FilterPage(BaseModel):
    offset: int = Field(ge=0, default=0)
    limit: int = Field(ge=0, default=10)
