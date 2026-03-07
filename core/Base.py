from pydantic import BaseModel

class Frame(BaseModel):
    x: int
    y: int
    w: int
    h: int
class Vec2D(BaseModel):
    x: float
    y: float