from fastapi import APIRouter, HTTPException, status

from api.schemas.auth import AuthResponse, LoginRequest, RegisterRequest, UserInfo
from auth.service import AuthError, login_user, register_user

router = APIRouter(prefix="/v1/auth", tags=["auth"])


@router.post("/register", response_model=AuthResponse, status_code=status.HTTP_201_CREATED)
def register(payload: RegisterRequest) -> AuthResponse:
    try:
        result = register_user(payload.username, payload.name, payload.password)
    except AuthError as exc:
        detail = str(exc)
        code = (
            status.HTTP_409_CONFLICT
            if "already exists" in detail.lower()
            else status.HTTP_400_BAD_REQUEST
        )
        raise HTTPException(status_code=code, detail=detail) from exc

    return AuthResponse(
        access_token=result["access_token"],
        token_type=result["token_type"],
        user=UserInfo(**result["user"]),
    )


@router.post("/login", response_model=AuthResponse)
def login(payload: LoginRequest) -> AuthResponse:
    try:
        result = login_user(payload.username, payload.password)
    except AuthError as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(exc),
        ) from exc

    return AuthResponse(
        access_token=result["access_token"],
        token_type=result["token_type"],
        user=UserInfo(**result["user"]),
    )
