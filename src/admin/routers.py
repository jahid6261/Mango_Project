from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.utils.db import get_db
from src.admin.schemas import (
    UpdateOrderStatusRequest,
    AdminAllOrdersResponse,
    AdminSingleOrderResponse,
)
from src.depends.admin_check import require_admin

from src.admin.service import (
    get_all_orders,
    get_order_by_id,
    update_order_status,
    get_dashboard
)


admin_routes = APIRouter(
    prefix="/admin",
    tags=["Admin"]
)


@admin_routes.get(
    "/orders",
    response_model=AdminAllOrdersResponse,
    status_code=status.HTTP_200_OK,
)
async def all_orders(
    db: AsyncSession = Depends(get_db),
    user=Depends(require_admin),
):
    return await get_all_orders(db)


@admin_routes.get(
    "/orders/{order_id}",
    response_model=AdminSingleOrderResponse,
    status_code=status.HTTP_200_OK,
)
async def get_order_id(
    order_id: int,
    db: AsyncSession = Depends(get_db),
    user=Depends(require_admin),
):
    return await get_order_by_id(order_id, db)


@admin_routes.patch(
    "/orders/{order_id}",
    status_code=status.HTTP_200_OK,
)
async def update_order(
    order_id: int,
    request: UpdateOrderStatusRequest,
    db: AsyncSession = Depends(get_db),
    user=Depends(require_admin),
):
    return await update_order_status(order_id, request, db)


@admin_routes.get(
    "/dashboard",
    status_code=status.HTTP_200_OK,
)
async def dashboard(
    db: AsyncSession = Depends(get_db),
    user=Depends(require_admin),
):
    return await get_dashboard(db)