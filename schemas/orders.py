from pydantic import BaseModel


class OrdersCreate(BaseModel):
    """order register request schema."""
    date: str
    time: str
    pet_name: str
    pet_species: str
    staff_id: int