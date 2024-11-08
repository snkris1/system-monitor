from ninja import ModelSchema, Schema
from pydantic import EmailStr

class LoginSchema(ModelSchema):
    email: EmailStr
    password: str


class RegisterSchema(ModelSchema):
    email: EmailStr
    password: str

