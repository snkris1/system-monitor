from ninja import ModelSchema, Schema
from pydantic import EmailStr

class LoginSchema(Schema):
    email: EmailStr
    password: str

class TokenSchema(Schema):
    access: str
    refresh: str

class RefreshSchema(Schema):
    refresh: str

class RegisterSchema(Schema):
    email: EmailStr
    password: str

class LogoutSchema(Schema):
    refresh_token: str

