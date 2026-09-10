from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.orders.models import Order, OrderStatus
from src.mango_product.models import MangoProduct
from src.admin.schemas import updateOrderstatusRequest


async def get_all_orders(db: AsyncSession):
    result = await db.execute(
        select(Order)
    )

    return result.scalars().all()


async def get_order_by_id(
    order_id: int,
    db: AsyncSession
):
    result = await db.execute(
        select(Order).where(Order.id == order_id)
    )

    order = result.scalar_one_or_none()

    if not order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Order not found"
        )

    return order


async def update_order_status(
    order_id: int,
    request: updateOrderstatusRequest,
    db: AsyncSession
):
    result = await db.execute(
        select(Order).where(
            Order.id == order_id
        )
    )

    order = result.scalar_one_or_none()

    if not order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Order not found"
        )

    # Already completed
    if order.status == OrderStatus.COMPLETED:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Order is already completed"
        )

    # Already cancelled
    if order.status == OrderStatus.CANCELLED:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cancelled order cannot be updated"
        )

    # Only Pending → Completed
    if request.status == OrderStatus.COMPLETED:

        result = await db.execute(
            select(MangoProduct).where(
                MangoProduct.id == order.product_id
            )
        )

        product = result.scalar_one_or_none()

        if not product:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Product not found"
            )

        # Check stock
        if product.stock < order.quantity:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Insufficient stock"
            )

        # Reduce stock
        product.stock -= order.quantity

        # Complete order
        order.status = OrderStatus.COMPLETED

    elif request.status == OrderStatus.CANCELLED:

        order.status = OrderStatus.CANCELLED

    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid order status"
        )

    try:
        await db.commit()
        await db.refresh(order)

    except Exception:
        await db.rollback()

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to update order status"
        )

    return {
        "success": True,
        "message": "Order status updated successfully",
        "data": order
    }