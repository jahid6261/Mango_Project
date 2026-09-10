from fastapi import HTTPException ,status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from decimal import Decimal

from src.orders.models import Order,OrderStatus,DeliveryZone
from src.orders.schemas import  OrderResponse,CheckoutSchema
from src.mango_product.models import MangoProduct
from src.users.models import UserModel
import traceback





async def checkout_order(
    checkout_data: CheckoutSchema,
    db: AsyncSession,
    user_id: int,
):

    # Get product
    result = await db.execute(
        select(MangoProduct).where(
            MangoProduct.id == checkout_data.product_id
        )
    )

    product = result.scalar_one_or_none()

    if product is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found",
        )

    # Check availability
    if not product.is_available:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Product is not available",
        )

    # Quantity
    quantity = Decimal(str(checkout_data.quantity))

    # Check stock
    if product.stock < quantity:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Insufficient stock",
        )

    # Calculate product total
    total_price = (
        Decimal(str(product.price)) * quantity
    )

    # Calculate delivery charge
    if checkout_data.city.strip().lower() == "dhaka":
      delivery_zone = "dhaka"
      delivery_charge = Decimal("100")
    else:
      delivery_zone = "outside_dhaka"
      delivery_charge = Decimal("150")
   

    # Calculate final price
    final_price = total_price + delivery_charge

    # Create order
    order = Order(
        user_id=user_id,
        product_id=product.id,
        quantity=quantity,
        total_price=total_price,
        delivery_zone=delivery_zone,
        delivery_charge=delivery_charge,
        final_price=final_price,
        status=OrderStatus.PENDING,
        full_name=checkout_data.full_name,
        email=checkout_data.email,
        phone_number=checkout_data.phone_number,
        city=checkout_data.city,
        postal_code=checkout_data.postal_code,
        address=checkout_data.address,
        note=checkout_data.note,
    )

    db.add(order)

    try:
        await db.commit()
        await db.refresh(order)

    except Exception as e:
      await db.rollback()
      print("ORDER CREATE ERROR:", type(e).__name__)
      print("ORDER CREATE ERROR:", str(e))
      raise HTTPException(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        detail=f"Failed to create order: {str(e)}",
    )

    return order



async def get_my_order(db: AsyncSession, user_id: int):

    result = await db.execute(
        select(UserModel).where(UserModel.id == user_id)
    )

    user = result.scalar_one_or_none()

    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    result = await db.execute(
        select(Order).where(Order.user_id == user_id)
    )

    orders = result.scalars().all()

    return [
        OrderResponse(
            id=order.id,
            user_id=order.user_id,
            product_id=order.product_id,
            quantity=order.quantity,
            total_price=float(order.total_price),
            status=order.status.value
        )
        for order in orders
    ]



async def get_order_by_id(db:AsyncSession,order_id:int,user_id:int):

    result =await db.execute(select(UserModel).
                             where(UserModel.id==user_id))
    user=result.scalar_one_or_none()

    if not user:
        raise HTTPException(status_code=404,detail='user not found')
    


    result=await db.execute(select(Order).where(Order.id==order_id,
                                                Order.user_id==user_id))
    
    order = result.scalar_one_or_none()

    if not order:
        raise HTTPException(status_code=404,detail="order not found")
    

    return OrderResponse(
        id=order.id,
        user_id=order.user_id,
        product_id=order.product_id,
        quantity=order.quantity,
        total_price=float(order.total_price),
        status=order.status.value
    )   


async def cancel_order(
    db: AsyncSession,
    order_id: int,
    user_id: int,
):
    # Find user's order
    result = await db.execute(
        select(Order).where(
            Order.id == order_id,
            Order.user_id == user_id,
        )
    )

    order = result.scalar_one_or_none()

    if not order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Order not found",
        )

    # Only pending orders can be cancelled
    if order.status != OrderStatus.PENDING:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Only pending orders can be cancelled",
        )

    # Cancel order
    order.status = OrderStatus.CANCELLED

    try:
        await db.commit()
        await db.refresh(order)

    except Exception:
        await db.rollback()

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to cancel order",
        )

    return {
        "message": "Order cancelled successfully",
        "order_id": order.id,
        "status": order.status.value,
    }