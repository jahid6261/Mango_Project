from decimal import Decimal
from typing import Optional
from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field
from fastapi import Form


# ========================
# Category Schemas
# ========================

class CategoryRequest(BaseModel):
    title: str = Field(..., max_length=150)
    slug: str = Field(..., max_length=150)
    description: str


class CategoryUpdateRequest(BaseModel):
    id: int
    title: str = Field(..., max_length=150)
    slug: str = Field(..., max_length=150)
    description: str


class CategoryBulkDeleteRequest(BaseModel):
    ids: list[int]


class CategoryResponse(BaseModel):
    id: int
    title: str
    slug: str
    description: str

    model_config = ConfigDict(from_attributes=True)


class CategoryPatchRequest(BaseModel):
    title: Optional[str] = Field(
        default=None,
        max_length=150
    )
    slug: Optional[str] = Field(
        default=None,
        max_length=150
    )
    description: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)


# ========================
# Product Schemas
# ========================

class MangoProductRequest(BaseModel):
    title: str = Field(..., max_length=200)
    slug: str = Field(..., max_length=200)
    description: str
    price: Decimal = Field(..., gt=0)
    quantity: float = Field(..., ge=0)
    stock: Decimal = Field(..., ge=0)
    is_available: bool = True
    category_id: int


class MangoProductUpdateRequest(BaseModel):
    title: str = Field(max_length=200)
    slug: str = Field(max_length=200)
    description: str
    price: Decimal = Field(gt=0)
    quantity: float = Field(ge=0)
    stock: Decimal = Field(ge=0)
    is_available: bool
    category_id: int

    model_config = ConfigDict(from_attributes=True)


class MangoProductPatchRequest(BaseModel):
    title: Optional[str] = Field(default=None, max_length=200)
    slug: Optional[str] = Field(default=None, max_length=200)
    description: Optional[str] = None
    price: Optional[Decimal] = Field(default=None, gt=0)
    quantity: Optional[float] = Field(default=None, ge=0)
    stock: Optional[Decimal] = Field(default=None, ge=0)
    is_available: Optional[bool] = None
    category_id: Optional[int] = None

    model_config = ConfigDict(from_attributes=True)


class ProductImageResponse(BaseModel):
    id: int
    image_url: str
    public_id: str

    model_config = ConfigDict(from_attributes=True)


class MangoProductResponse(BaseModel):
    id: int
    title: str
    slug: str
    description: str
    price: Decimal
    quantity: float
    stock: Decimal
    is_available: bool
    category_id: int
    images: list[ProductImageResponse] = Field(default_factory=list)

    model_config = ConfigDict(from_attributes=True)


class MangoProductDeleteBulkRequest(BaseModel):
    ids: list[int]


# ========================
# Review Schemas
# ========================

class ReviewRequest(BaseModel):
    product_id: int
    rating: int = Field(..., ge=1, le=5, description="Rating must be between 1 and 5")
    comment: Optional[str] = Field(default=None, max_length=500)


class ReviewResponse(BaseModel):
    id: int
    product_id: int
    user_id: int
    rating: int
    comment: Optional[str]
    created_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)