from pydantic import BaseModel


class Estate(BaseModel):
    name: str | None
    description: str | None
    id: str