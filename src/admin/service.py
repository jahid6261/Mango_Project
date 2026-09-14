from fastapi import HTTPException, status
from sqlalchemy import select,func
from sqlalchemy.ext.asyncio import AsyncSession

from src.orders.models import Order, OrderStatus
from src.mango_product.models import MangoProduct,Category
from src.users.models import UserModel
from src.admin.schemas import UpdateOrderStatusRequest
from src.utils.email import send_order_completed_email

async def get_all_orders(db: AsyncSession):

    result = await db.execute(
        select(Order)
    )

    orders = result.scalars().all()

    return {
        "success": True,
        "total_orders": len(orders),
        "orders": [
            {
                "order_id": order.id,

                "customer": {
                    "user_id": order.user_id,
                    "name": order.full_name,
                    "email": order.email,
                    "phone": order.phone_number,
                },

                "product": {
                    "product_id": order.product_id,
                    "quantity": float(order.quantity),
                },

                "payment": {
                    "method": "Cash on Delivery",
                    "product_total": float(order.total_price),
                    "delivery_charge": float(order.delivery_charge),
                    "final_price": float(order.final_price),
                },

                "delivery": {
                    "zone": order.delivery_zone,
                    "city": order.city,
                    "postal_code": order.postal_code,
                    "address": order.address,
                    "note": order.note,
                },

                "status": order.status.value,
                "created_at": order.created_at,
                "updated_at": order.updated_at,
            }
            for order in orders
        ]
    }
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

    return {
        "success": True,
        "data": {
            "order_id": order.id,

            "customer": {
                "user_id": order.user_id,
                "name": order.full_name,
                "email": order.email,
                "phone": order.phone_number,
            },

            "product": {
                "product_id": order.product_id,
                "quantity": float(order.quantity),
            },

            "payment": {
                "method": "Cash on Delivery",
                "product_total": float(order.total_price),
                "delivery_charge": float(order.delivery_charge),
                "final_price": float(order.final_price),
            },

            "delivery": {
                "zone": order.delivery_zone,
                "city": order.city,
                "postal_code": order.postal_code,
                "address": order.address,
                "note": order.note,
            },

            "status": order.status.value,
            "created_at": order.created_at,
            "updated_at": order.updated_at,
        }
    }

async def update_order_status(
    order_id: int,
    request: UpdateOrderStatusRequest,
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

    # Pending → Completed
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

    # Send email only after successful completion
    if order.status == OrderStatus.COMPLETED:
     try:
        email_result = send_order_completed_email(
            to_email=order.email,
            first_name=order.full_name,
            order_id=order.id,
            product_total=order.total_price,
            delivery_charge=order.delivery_charge,
            final_price=order.final_price,
        )

        print("ORDER COMPLETED EMAIL RESULT:", email_result)

     except Exception as e:
        print("ORDER COMPLETED EMAIL ERROR:", type(e).__name__)
        print("ORDER COMPLETED EMAIL ERROR:", str(e))
    
    return {
        "success": True,
        "message": "Order status updated successfully",
        "data": order
    }





async def get_dashboard(db: AsyncSession):

    total_users = await db.scalar(
        select(func.count(UserModel.id))
    )

    total_products = await db.scalar(
        select(func.count(MangoProduct.id))
    )

    total_categories = await db.scalar(
        select(func.count(Category.id))
    )

    total_orders = await db.scalar(
        select(func.count(Order.id))
    )

    pending_orders = await db.scalar(
        select(func.count(Order.id)).where(
            Order.status == OrderStatus.PENDING
        )
    )

    total_sales = await db.scalar(
        select(
            func.coalesce(
                func.sum(Order.final_price),
                0
            )
        ).where(
            Order.status == OrderStatus.COMPLETED
        )
    )

    return {
        "success": True,
        "data": {
            "total_users": total_users or 0,
            "total_products": total_products or 0,
            "total_categories": total_categories or 0,
            "total_orders": total_orders or 0,
            "pending_orders": pending_orders or 0,
            "total_sales": total_sales or 0,
        }
    }