from fastapi import Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jwt.exceptions import InvalidTokenError
from sqlalchemy.orm import Session

from app.core.security import decode_token
from app.db.session import get_db
from app.models.user import User
from app.services.user_service import get_user_by_email

# HTTPBearer đọc header "Authorization: Bearer <token>" đúng theo API仕様
bearer_scheme = HTTPBearer()


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
    db: Session = Depends(get_db),
) -> User:
    token = credentials.credentials  # lấy phần token, bỏ chữ "Bearer "
    try:
        payload = decode_token(token)
        email = payload.get("email")
        if email is None:
            raise HTTPException(status_code=401, detail="Invalid token payload")
    except InvalidTokenError:
        # Token sai định dạng, sai chữ ký, hoặc hết hạn (exp) đều rơi vào đây
        raise HTTPException(status_code=401, detail="Invalid or expired token")

    user = get_user_by_email(db, email)
    if user is None:
        raise HTTPException(status_code=401, detail="User not found")
    return user


def get_current_admin(current_user: User = Depends(get_current_user)) -> User:
    # Dùng cho các route chỉ admin mới được phép (nếu sau này cần)
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Not enough permissions")
    return current_user