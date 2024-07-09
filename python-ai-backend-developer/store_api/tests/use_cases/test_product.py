from store.usecases.product import product_usecase
from store.core.schemas.product import ProductOut, ProductUpdateOut
from store.core.exceptions import NotFoundException
from typing import List

from uuid import UUID
import pytest


async def test_usecases_should_return_success(product_in):
    result = await product_usecase.create(body=product_in)
    assert isinstance(result, ProductOut)
    assert result.name == "Iphone 14 Pro Max"


async def test_usecases_get_should_return_success(product_id):
    result = await product_usecase.get(id=product_id)
    assert isinstance(result, ProductOut)
    assert result.name == "Iphone 14 Pro Max"


async def test_usecases_get_should_not_found():
    with pytest.raises(NotFoundException) as err:
        id = UUID("fce6cc37-10b9-4a8e-a8b2-977df327001b")
        await product_usecase.get(id=id)
    assert err.value.message == f"Product not found with filter 'id': {id}"


async def test_usecases_query_should_return_success():
    result = await product_usecase.query()
    assert isinstance(result, List)


async def test_usecases_update_should_return_success(product_id, product_up):
    product_up.price = 7500.0
    result = await product_usecase.update(id=product_id, body=product_up)
    assert isinstance(result, ProductUpdateOut)
