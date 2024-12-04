from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException
from user_login.models.user import User as UserModel, Role
from user_login.schemas.user import UserLoginRequest
from user_login.client.xquare_client import XquareClient
from user_login.security.jwt import JWTTokenProvider
from uuid import uuid4

class UserLoginService:
    def __init__(self, db: Session, xquare_client: XquareClient, jwt_provider: JWTTokenProvider):
        self.db = db
        self.xquare_client = xquare_client
        self.jwt_provider = jwt_provider

    def login(self, user_login_request: UserLoginRequest) -> str:
        account_id = user_login_request.account_id

        xquare_user_data = self.xquare_client.xquare_user(
            account_id=user_login_request.account_id,
            password=user_login_request.password
        )
        if not self.db.query(UserModel).filter_by(account_id=account_id).first():
            user = UserModel(
                            id=uuid4(),
                            xquare_id=xquare_user_data["id"],
                            account_id=xquare_user_data["account_id"],
                            name=xquare_user_data["name"],
                            grade=xquare_user_data["grade"],
                            class_num=xquare_user_data["class_num"],
                            num=xquare_user_data["num"],
                            birth_day=xquare_user_data["birth_day"],
                            device_token=None,
                            profile=xquare_user_data.get("profile", None),  # profile 기본값을 None으로 설정
                            role=Role[xquare_user_data.get("role", "STU")]  # role 기본값을 "STU"로 설정 (필요에 따라 조정)
                        )

            self.db.add(user)
            self.db.commit()
        else:
            user = self.db.query(UserModel).filter_by(account_id=account_id).first()

        return self.jwt_provider.generate_token(account_id=user.account_id, role=user.role.name)
