from pydantic import BaseModel


class CreateLaptopModel(BaseModel):
    model: str
    developer: str


class Laptop:
    def __init__(self, id: int, model: str, developer: str):
        self.id = id
        self.model = model
        self.developer = developer
