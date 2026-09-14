from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.orders.schemas import CheckoutSchema, OrderResponse
from src.orders import services
from src.utils.db import get_db
from src.depends.user_check import get_current_user
from src.users.models import UserModel


order_routes = APIRouter(
    prefix="/orders",
    tags=["Orders"]
)


@order_routes.post(
    "/checkout",
    response_model=OrderResponse
)
async def order_create(
    checkout_data: CheckoutSchema,
    db: AsyncSession = Depends(get_db),
    current_user: UserModel = Depends(get_current_user),
):
    return await services.create_order(
        checkout_data=checkout_data,
        db=db,
        current_user=current_user,
    )


@order_routes.get(
    "/my-orders",
    response_model=list[OrderResponse]
)
async def get_my_order(
    db: AsyncSession = Depends(get_db),
    current_user: UserModel = Depends(get_current_user),
):
    return await services.get_my_order(
        db=db,
        current_user=current_user,
    )


@order_routes.get(
    "/{order_id}",
    response_model=OrderResponse
)
async def get_order_by_id(
    order_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: UserModel = Depends(get_current_user),
):
    return await services.get_order_by_id(
        db=db,
        order_id=order_id,
        current_user=current_user,
    )


@order_routes.patch("/{order_id}/cancel")
async def cancel_order(
    order_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: UserModel = Depends(get_current_user),
):
    return await services.cancel_order(
        db=db,
        order_id=order_id,
        current_user=current_user,
    )