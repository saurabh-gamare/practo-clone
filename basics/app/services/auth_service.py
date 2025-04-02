import os
from dotenv import load_dotenv
from datetime import timedelta, datetime
from typing import Annotated
from fastapi import Depends, HTTPException
from starlette import status
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from database import db_dependency as db


from models.auth import User
from models.profile import Profile


load_dotenv()
SECRET_KEY = os.getenv("SECRET_KEY") 
ALGORITHM = 'HS256'

bcrypt_context = CryptContext(schemes=['bcrypt'], deprecated='auto')
oauth2_bearer = OAuth2PasswordBearer(tokenUrl='auth/login')   # 'auth/login' => API endpoint


class CreateUser:

    def check_if_user_exists(self, db, request):
        user = db.query(User).filter(User.username==request.username).first()
        if user:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='User already exists.')

    async def create_user(self, db, request):
        self.check_if_user_exists(db, request)

        user = User(
            username=request.username,
            hashed_password=bcrypt_context.hash(request.password),
            role=request.role
        )
        db.add(user)
        db.commit()

        return {"user_id": user.id}


class Login:

    def authenticate_user(self, username: str, password: str, db):
        user = db.query(User).filter(User.username == username).first()
        if not user:
            return False
        if not bcrypt_context.verify(password, user.hashed_password):
            return False
        return user

    def create_access_token(self, username: str, user_id: int, role: str, expires_delta: timedelta):
        encode = {'sub': username, 'id': user_id, 'role': role}
        expires = datetime.now() + expires_delta
        encode.update({'exp': expires})
        return jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)

    async def login(self, form_data, db):
        user = self.authenticate_user(form_data.username, form_data.password, db)
        if not user:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Could not validate user.')
        token = self.create_access_token(user.username, user.id, user.role.name, timedelta(minutes=20))

        return {'access_token': token, 'token_type': 'bearer'}


class CurrentUser:

    async def get_current_user(self, token: Annotated[str, Depends(oauth2_bearer)]):
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            username: str = payload.get('sub')
            user_id: int = payload.get('id')
            role: str = payload.get('role')
            if username is None or user_id is None:
                raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Could not validate user')
            return {'username': username, 'id': user_id, 'role': role}
        except JWTError:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Could not validate user.')
        
    def check_permission(self, allowed_roles: list):
        def role_checker(user: dict = Depends(self.get_current_user)):
            if user.get('role') not in allowed_roles:
                raise HTTPException(
                    status_code=403, detail="Permission denied"
                )
        return role_checker