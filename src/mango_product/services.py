from sqlalchemy.ext.asyncio import AsyncSession
from src.mango_product.models import Category, MangoProduct, Review, ProductImage
from src.mango_product.schemas import (
    CategoryRequest,
    MangoProductRequest,
    CategoryResponse,
    CategoryUpdateRequest,
    MangoProductResponse,
    CategoryBulkDeleteRequest,
    MangoProductDeleteBulkRequest,
    MangoProductPatchRequest,
    MangoProductUpdateRequest,
    ReviewRequest,
    ReviewResponse,
    CategoryPatchRequest,
)
from src.utils.db import DB_Session
from sqlalchemy import select, update, delete
from fastapi import HTTPException, status
from sqlalchemy import update, bindparam, or_, and_
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from src.orders.models import Order, OrderStatus
from src.utils.cloudinary import upload_image,delete_image
from fastapi import UploadFile
from sqlalchemy.orm import selectinload



# ========================
# Category CRUD Operations
# ========================

async def create_category(request: CategoryRequest, db: AsyncSession):
    new_category = Category(
        title=request.title.strip(),
        slug=request.slug.strip(),
        description=request.description.strip()
    )

    db.add(new_category)

    try:
        await db.commit()
        await db.refresh(new_category)
    except Exception as e:
        await db.rollback()
        print("CATEGORY CREATE ERROR:", e)
        raise

        

    return CategoryResponse(
        id=new_category.id,
        title=new_category.title,
        slug=new_category.slug,
        description=new_category.description
    )


async def create_bulk_categories(
    request: list[CategoryRequest],
    db: AsyncSession
):
    categories = [
        Category(**item.model_dump())
        for item in request
    ]

    db.add_all(categories)

    try:
        await db.commit()
        for category in categories:
            await db.refresh(category)
    except IntegrityError:
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Category already exists"
        )
    except SQLAlchemyError:
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create categories"
        )

    return categories


async def all_category(db: AsyncSession):
    query = select(Category)
    result = await db.execute(query)
    return result.scalars().all()


async def get_category_by_id(category_id: int, db: AsyncSession):
    query = select(Category).where(Category.id == category_id)
    result = await db.execute(query)
    return result.scalars().first()


async def update_category(category_id: int, request: CategoryUpdateRequest, db: AsyncSession):
    await db.execute(
        update(Category)
        .where(Category.id == category_id)
        .values(
            title=request.title.strip(),
            slug=request.slug.strip(),
            description=request.description.strip()
        )
    )

    await db.commit()
    return {"message": "Category updated successfully"}


async def patch_category(
    category_id: int,
    request: CategoryPatchRequest,
    db: AsyncSession
):
    update_data = request.model_dump(exclude_unset=True)

    if not update_data:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No data provided"
        )

    if "title" in update_data:
        update_data["title"] = update_data["title"].strip()

    if "slug" in update_data:
        update_data["slug"] = update_data["slug"].strip()

    if "description" in update_data:
        update_data["description"] = update_data["description"].strip()

    try:
        result = await db.execute(
            update(Category)
            .where(Category.id == category_id)
            .values(**update_data)
        )

        if result.rowcount == 0:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Category not found"
            )

        await db.commit()

    except IntegrityError:
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Slug already exists"
        )
    except SQLAlchemyError:
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to update category"
        )

    return {"message": "Category updated successfully"}


async def category_delete(category_id: int, db: AsyncSession):
    query = delete(Category).where(Category.id == category_id)
    result = await db.execute(query)

    if result.rowcount == 0:
        raise HTTPException(status_code=404, detail="Category is not found")

    await db.commit()
    return {'message': "Category is deleted successfully"}


async def category_bulk_delete(request: CategoryBulkDeleteRequest, db: AsyncSession):
    if not request.ids:
        raise HTTPException(
            status_code=400,
            detail="No ids provided"
        )

    query = delete(Category).where(Category.id.in_(request.ids))
    result = await db.execute(query)

    await db.commit()

    return {
        "message": f"{result.rowcount} category deleted successfully"
    }


# ========================
# Product CRUD Operations
# ========================

async def product_create(
    request: MangoProductRequest,
    db: AsyncSession
):
    new_product = MangoProduct(
        title=request.title.strip(),
        slug=request.slug.strip(),
        description=request.description.strip(),
        price=request.price,
        quantity=request.quantity,
        stock=request.stock,
        is_available=request.is_available,
        category_id=request.category_id
    )

    db.add(new_product)

    try:
        await db.commit()
        await db.refresh(new_product)
    except IntegrityError:
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Slug already exists"
        )
    except SQLAlchemyError:
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create product"
        )

    return new_product


async def product_bulk(
    request: list[MangoProductRequest],
    db: AsyncSession
):
    products = [
        MangoProduct(**item.model_dump())
        for item in request
    ]

    try:
        db.add_all(products)
        await db.commit()

        return {
            "message": "Products created successfully",
            "count": len(products)
        }

    except IntegrityError:
        await db.rollback()
        raise HTTPException(
            status_code=400,
            detail="Duplicate slug or invalid data"
        )

    except SQLAlchemyError:
        await db.rollback()
        raise HTTPException(
            status_code=500,
            detail="Failed to create products"
        )


# ========================
# Product Image Operations
# =====
async def product_upload_image(
    product_id: int,
    image: UploadFile,
    db: AsyncSession,
):
    result = await db.execute(
        select(MangoProduct).where(
            MangoProduct.id == product_id
        )
    )

    product = result.scalar_one_or_none()

    if product is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found",
        )

    try:
        uploaded = await upload_image(image)

        product_image = ProductImage(
            product_id=product.id,
            image_url=uploaded["image_url"],
            public_id=uploaded["public_id"],
        )

        db.add(product_image)

        await db.commit()
        await db.refresh(product_image)

        return product_image

    except Exception:
        await db.rollback()

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to upload product image",
        )


async def delete_product_image(
    image_id: int,
    db: AsyncSession,
):
    image = await db.scalar(
        select(ProductImage)
        .where(ProductImage.id == image_id)
    )

    if image is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Image not found",
        )

    try:
        await delete_image(image.public_id)

        await db.delete(image)
        await db.commit()

        return {
            "message": "Image deleted successfully."
        }

    except SQLAlchemyError:
        await db.rollback()

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Database error occurred.",
        )

    except Exception as e:
        await db.rollback()

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to delete image from Cloudinary: {str(e)}",
        )
    

# ========================
# Product Retrieval Operations
# ========================

async def get_products_for_ai(db: AsyncSession):
    query = select(MangoProduct).where(MangoProduct.is_available == True)
    result = await db.execute(query)
    return result.scalars().all()


async def get_products_processed(
    db: AsyncSession,
    product_id: int = None,
    search_name: str = None,
    min_price: float = None,
    max_price: float = None
) -> list[MangoProduct]:
    query = (
        select(MangoProduct)
        .options(selectinload(MangoProduct.images))
    )

    filters = []

    if product_id is not None:
        filters.append(MangoProduct.id == product_id)

    if search_name and search_name.strip():
        search_term = f"%{search_name.strip()}%"
        filters.append(MangoProduct.title.ilike(search_term))

    if min_price is not None:
        filters.append(MangoProduct.price >= min_price)

    if max_price is not None:
        filters.append(MangoProduct.price <= max_price)

    if filters:
        query = query.where(and_(*filters))

    result = await db.execute(query)
    products = result.scalars().all()

    if not products:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found"
        )

    return products


async def get_all_products(
    db: AsyncSession
) -> list[MangoProduct]:
    query = (
        select(MangoProduct)
        .options(selectinload(MangoProduct.images))
    )

    result = await db.execute(query)
    return result.scalars().all()

async def put_product(
    product_id: int,
    request: MangoProductUpdateRequest,
    db: AsyncSession,
):
    product = await db.scalar(
        select(MangoProduct).where(MangoProduct.id == product_id)
    )

    if product is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found",
        )

    product.title = request.title.strip()
    product.slug = request.slug.strip()
    product.description = request.description.strip()
    product.price = request.price
    product.stock=request.stock
    product.quantity=request.quantity
    product.is_available = request.is_available
    product.category_id = request.category_id

    await db.commit()
    await db.refresh(product)

    return product

async def patch_product(
    product_id: int,
    request: MangoProductPatchRequest,
    db: AsyncSession,
):
    product = await db.scalar(
        select(MangoProduct).where(MangoProduct.id == product_id)
    )

    if product is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found",
        )

    if request.title is not None:
        product.title = request.title.strip()

    if request.slug is not None:
        product.slug = request.slug.strip()

    if request.description is not None:
        product.description = request.description.strip()

    if request.price is not None:
        product.price = request.price

    if request.quantity is not None:
        product.quantity=request.quantity

    if request.stock is not None:
        product.stock=request.stock


    if request.is_available is not None:
        product.is_available = request.is_available

    if request.category_id is not None:
        product.category_id = request.category_id

    await db.commit()
    await db.refresh(product)

    return product

async def product_delete(product_id: int, db: AsyncSession):

    query = delete(MangoProduct).where(MangoProduct.id == product_id)
    result = await db.execute(query)

    if result.rowcount == 0:
        raise HTTPException(
            status_code=404,
            detail="product is not found"
        )

    await db.commit()

    return {
        "message": "product is deleted successfully"
    }
    



async def product_delete_bulk(request: MangoProductDeleteBulkRequest, db: AsyncSession):
    if not request.ids:
        raise HTTPException(
            status_code=400,
            detail="No ids provided"
        )

    query = delete(MangoProduct).where(MangoProduct.id.in_(request.ids))
    result = await db.execute(query)

    await db.commit()

    return {"message": f"{result.rowcount} product deleted successfully"}


# ========================
# Review Operations
# ========================

async def create_review(request:ReviewRequest, user_id: int, db: AsyncSession):
    product = await db.get(MangoProduct, request.product_id)

    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found"
        )

    result = await db.execute(
        select(Order).where(
            Order.user_id == user_id,
            Order.product_id == request.product_id,
            Order.status == OrderStatus.COMPLETED
        )
    )

    order = result.scalars().first()

    if not order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="You can review only completed orders"
        )

    result = await db.execute(
        select(Review).where(
            Review.user_id == user_id,
            Review.product_id == request.product_id
        )
    )

    if result.scalars().first():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="You have already reviewed this product."
        )

    review = Review(
        user_id=user_id,
        product_id=request.product_id,
        rating=request.rating,
        comment=request.comment
    )

    db.add(review)
    await db.commit()
    await db.refresh(review)

    return review