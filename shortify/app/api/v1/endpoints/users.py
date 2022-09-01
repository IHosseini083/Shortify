from typing import Any, Dict, Optional

from fastapi import APIRouter, Body, Depends, HTTPException, Query, status
from pydantic.networks import EmailStr

from shortify.app import schemas
from shortify.app.api.v1.deps import (
    get_current_active_superuser,
    get_current_active_user,
)
from shortify.app.core.security import get_password_hash
from shortify.app.models import User

router = APIRouter()


@router.get("/", response_model=schemas.Paginated[schemas.User])
async def get_users(
    page: int = Query(1, ge=1),
    per_page: int = Query(10, ge=1, le=100),
    _=Depends(get_current_active_superuser),
) -> Dict[str, Any]:
    results = await User.find().skip((page - 1) * per_page).limit(per_page).to_list()
    return {
        "page": page,
        "per_page": per_page,
        "total": await User.count(),
        "results": results,
    }


@router.post("/", response_model=schemas.User, status_code=status.HTTP_201_CREATED)
async def create_user(
    user_in: schemas.UserCreate,
    _=Depends(get_current_active_superuser),
) -> User:
    """Create new user in the database."""
    user = await User.get_by_username(username=user_in.username)
    if user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="The user associated with this username already exists",
        )
    data = user_in.dict()
    data["hashed_password"] = get_password_hash(data.pop("password"))
    return await User(**data).insert()


@router.get("/me", response_model=schemas.User)
def get_current_user(user: User = Depends(get_current_active_user)) -> User:
    """Get current active user details."""
    return user


@router.patch("/me", response_model=schemas.User)
async def update_current_user(
    password: Optional[str] = Body(None),
    email: Optional[EmailStr] = Body(None),
    user: User = Depends(get_current_active_user),
) -> User:
    """Update current user using provided data."""
    if password is not None:
        user.hashed_password = get_password_hash(password)
    if email is not None:
        user.email = email
    await user.save_changes()
    return user


@router.get("/{username}", response_model=schemas.User)
async def get_user_by_username(
    username: str,
    _=Depends(get_current_active_superuser),
) -> User:
    """Get a specific user by username."""
    user = await User.get_by_username(username=username)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="The user with this username does not exist",
        )
    return user


@router.patch("/{username}", response_model=schemas.User)
async def update_user_by_username(
    username: str,
    user_in: schemas.UserUpdate,
    _=Depends(get_current_active_superuser),
) -> User:
    """Update a specific user by username."""
    user = await User.get_by_username(username=username)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="The user with this username does not exist",
        )
    update_data = user_in.dict(exclude_unset=True)
    await user.set(update_data)
    return user
