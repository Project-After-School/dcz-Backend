from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from user_login.schemas.user import UserLoginRequest
from user_login.service.user_login_service import UserLoginService
from user_login.client.xquare_client import XquareClient
from user_login.security.jwt import JWTTokenProvider
from user_login.database import get_db  # 데이터베이스 연결 종속성
from user_login.exceptions import UserNotFoundException, PasswordMissMatchException

router = APIRouter()

@router.post("/user/login")
def login(user_login_request: UserLoginRequest, db: Session = Depends(get_db)):
    try:
        user_login_service = UserLoginService(
            db=db, 
            xquare_client=XquareClient(base_url="https://prod-server.xquare.app/dsm-login/user"),
            jwt_provider=JWTTokenProvider()
        )
        token = user_login_service.login(user_login_request)
        return {"access_token": token, "token_type": "bearer"}
    except UserNotFoundException:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    except PasswordMissMatchException:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect password")
    except Exception as e:
        print(f"Unexpected error: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")