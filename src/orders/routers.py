from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.orders.schemas import CheckoutSchema, OrderResponse
from src.orders import services
from src.utils.db import get_db
from src.depends.auth_depends import require_user_id

order_routes = APIRouter(
    prefix="/orders",
    tags=["Orders"] 
)



@order_routes.post("/checkout",response_model=OrderResponse)

async def checkout(
    checkout_data:CheckoutSchema,
    db:AsyncSession=Depends(get_db),
    user=Depends(require_user_id),

):

    return await services.checkout_order(
        checkout_data=checkout_data,
        db=db,
        user_id=user["user_id"],
      
    )





@order_routes.get("/my-orders")
async def get_my_order(
    user = Depends(require_user_id),
    db: AsyncSession = Depends(get_db)
):
    return await services.get_my_order(
        user_id=user['user_id'],
        db=db
    )



@order_routes.get("/{order_id}")

async def get_order_by_id(order_id:int,user=Depends(require_user_id),
                          db:AsyncSession=Depends(get_db)):
    
    return await services.get_order_by_id(

        db=db,
        order_id=order_id,
        user_id=user['user_id']
    )



@order_routes.patch("/orders/{order_id}/cancel")
async def cancel_order(
    order_id: int,
    db: AsyncSession = Depends(get_db),
    user=Depends(require_user_id),
):
    return await services.cancel_order(
        db=db,
        order_id=order_id,
        user_id=user["user_id"],
    )

    



