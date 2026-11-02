from datetime import datetime, timedelta, timezone

from jose import jwt, JWTError
from passlib.context import CryptContext
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from .config import settings
from .database import get_db
from .models import User


ALGORITHM = "HS256"

pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto"
)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(password: str, hashed: str) -> bool:
    return pwd_context.verify(password, hashed)


def create_access_token(data: dict) -> str:
    to_encode = data.copy()

    expire = datetime.now(timezone.utc) + timedelta(
        minutes=settings.access_token_expire_minutes
    )

    to_encode.update({"exp": expire})

    return jwt.encode(
        to_encode,
        settings.secret_key,
        algorithm=ALGORITHM
    )


def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Login yoki parol noto'g'ri",
        headers={"WWW-Authenticate": "Bearer"}
    )

    try:
        payload = jwt.decode(
            token,
            settings.secret_key,
            algorithms=[ALGORITHM]
        )

        user_id = payload.get("sub")

        if user_id is None:
            raise credentials_exception

        user = db.query(User).filter(
            User.id == int(user_id)
        ).first()

        if not user or not user.is_active:
            raise credentials_exception

        return user

    except (JWTError, ValueError, TypeError):
        raise credentials_exception


def require_roles(*roles):
    def role_checker(
        current_user: User = Depends(get_current_user)
    ):
        if current_user.role not in roles:
            raise HTTPException(
                status_code=403,
                detail="Sizda ruxsat mavjud emas"
            )

        return current_user

    return role_checker