from fastapi import APIRouter, Depends, HTTPException, status, Query, File, UploadFile
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional

from src.utils.db import get_db
from src.mango_product import services
from src.mango_product.schemas import (
    CategoryResponse,
    CategoryRequest,
    CategoryUpdateRequest,
    CategoryBulkDeleteRequest,
    MangoProductRequest,
    MangoProductResponse,
    MangoProductDeleteBulkRequest,
    ReviewRequest,
    ReviewResponse,
    CategoryPatchRequest,
    MangoProductPatchRequest,
    MangoProductUpdateRequest,
)
from src.depends.admin_check import require_admin
from src.depends.auth_depends import require_user_id


# ========================
# Category Routes
# ========================

category_router = APIRouter(prefix="/categories", tags=["Categories"])


@category_router.post("", response_model=CategoryResponse)
async def create_category(
    request: CategoryRequest,
    user=Depends(require_admin),
    db: AsyncSession = Depends(get_db)
):
    return await services.create_category(request, db)


@category_router.post("/bulk", response_model=list[CategoryResponse])
async def create_bulk_categories(
    request: list[CategoryRequest],
    user=Depends(require_admin),
    db: AsyncSession = Depends(get_db)
):
    return await services.create_bulk_categories(request, db)


@category_router.get("", response_model=list[CategoryResponse])
async def get_all_categories(
    db: AsyncSession = Depends(get_db)
):
    return await services.all_category(db)


@category_router.get("/{category_id}", response_model=CategoryResponse)
async def get_category_by_id(
    category_id: int,
    db: AsyncSession = Depends(get_db)
):
    return await services.get_category_by_id(category_id, db)


@category_router.put("/{category_id}")
async def update_category(
    category_id: int,
    request: CategoryUpdateRequest,
    user=Depends(require_admin),
    db: AsyncSession = Depends(get_db)
):
    return await services.update_category(category_id, request, db)


@category_router.patch("/{category_id}")
async def patch_category(
    category_id: int,
    request: CategoryPatchRequest,
    user=Depends(require_admin),
    db: AsyncSession = Depends(get_db)
):
    return await services.patch_category(category_id, request, db)

@category_router.delete("/bulk")
async def delete_categories_bulk(
    request: CategoryBulkDeleteRequest,
    user=Depends(require_admin),
    db: AsyncSession = Depends(get_db)
):
    return await services.category_bulk_delete(request, db)


@category_router.delete("/{category_id}")
async def delete_category(
    category_id: int,
    user=Depends(require_admin),
    db: AsyncSession = Depends(get_db)
):
    return await services.category_delete(category_id, db)





# ========================
# Product Routes
# ========================

mango_product_routes = APIRouter(prefix="/products", tags=["Products"])

@mango_product_routes.post("/bulk")
async def create_products_bulk(
    request: list[MangoProductRequest],
    user=Depends(require_admin),
    db: AsyncSession = Depends(get_db)
):
    return await services.product_bulk(request, db)

@mango_product_routes.post("/create", response_model=MangoProductResponse)
async def create_product(
    request: MangoProductRequest,
    user=Depends(require_admin),
    db: AsyncSession = Depends(get_db)
):
    return await services.product_create(request, db)





@mango_product_routes.post("/{product_id}/images")
async def upload_product_image(
    product_id: int,
    image: UploadFile = File(...),
    user=Depends(require_admin),
    db: AsyncSession = Depends(get_db),
):
    return await services.product_upload_image(
        product_id,
        image,
        db,
    )


@mango_product_routes.delete("/images/{image_id}")
async def delete_product_image(
    image_id: int,
    user=Depends(require_admin),
    db: AsyncSession = Depends(get_db),
):
    return await services.delete_product_image(
        image_id,
        db,
    )

@mango_product_routes.get("/search", response_model=list[MangoProductResponse])
async def search_products(
    product_id: Optional[int] = Query(None, description="Search by product ID"),
    search_name: Optional[str] = Query(None, description="Search by product name (case-insensitive)"),
    min_price: Optional[float] = Query(None, description="Minimum price filter"),
    max_price: Optional[float] = Query(None, description="Maximum price filter"),
    db: AsyncSession = Depends(get_db)
):
    return await services.get_products_processed(
        db=db,
        product_id=product_id,
        search_name=search_name,
        min_price=min_price,
        max_price=max_price
    )


@mango_product_routes.get("/all", response_model=list[MangoProductResponse])
async def get_all_products(
    db: AsyncSession = Depends(get_db)
):
    return await services.get_all_products(db)

@mango_product_routes.put("/{product_id}")
async def update_product(
    product_id: int,
    request: MangoProductUpdateRequest,
    db: AsyncSession = Depends(get_db),
):
    return await services.put_product(
        product_id=product_id,
        request=request,
        db=db,
    )


@mango_product_routes.patch("/{product_id}")
async def patch_product(
    product_id: int,
    request: MangoProductPatchRequest,
    db: AsyncSession = Depends(get_db),
):
    return await services.patch_product(
        product_id=product_id,
        request=request,
        db=db,)

@mango_product_routes.delete("/bulk")
async def delete_products_bulk(
    request: MangoProductDeleteBulkRequest,
    user=Depends(require_admin),
    db: AsyncSession = Depends(get_db)
):
    return await services.product_delete_bulk(request, db)
@mango_product_routes.delete("/{product_id}")
async def product_delete(product_id:int,
                         user=Depends(require_admin),
                         db:AsyncSession=Depends(get_db)):
    return await services.product_delete(
        product_id,db
    )




# ========================
# Review Routes
# ========================

@mango_product_routes.post("/reviews", response_model=ReviewResponse)
async def create_product_review(
    request: ReviewRequest,
    db: AsyncSession = Depends(get_db),
    user=Depends(require_user_id)
):
    return await services.create_review(
        request=request,
        user_id=user['user_id'],
        db=db
    )