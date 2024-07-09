from store.core.schemas.base import BaseSchemaMixin
from pydantic import Field
from typing import Optional


class ProductBase(BaseSchemaMixin):
    name: str = Field(description="Product name")
    quantity: int = Field(description="Product quantity")
    price: float = Field(description="Product price")
    status: bool = Field(description="Product status")


class ProductIn(ProductBase, BaseSchemaMixin):
    ...


class ProductOut(ProductIn):
    ...


class ProductUpdate(ProductBase):
    quantity: Optional[int] = Field(None, description="Product quantity")
    price: Optional[float] = Field(None, description="Product price")
    status: Optional[bool] = Field(None, description="Product status")


class ProductUpdateOut(ProductUpdate):
    ...
