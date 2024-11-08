from ninja import ModelSchema, Schema
from pydantic import EmailStr

class LoginSchema(ModelSchema):
    email: EmailStr
    password: str

class TokenSchema(ModelSchema):
    access: str
    refresh: str

class RefreshSchema(ModelSchema):
    refresh: str

class RegisterSchema(ModelSchema):
    email: EmailStr
    password: str

