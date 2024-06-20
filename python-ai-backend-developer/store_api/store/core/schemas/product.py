from store.core.schemas.base import BaseSchemaMixin
from pydantic import Field


class ProductIn(BaseSchemaMixin):
    name: str = Field(description="Product name")
    quantity: int = Field(description="Product quantity")
    price: float = Field(description="Product price")
    status: bool = Field(description="Product status")
