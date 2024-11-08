from django.contrib.auth import get_user_model
from ninja import Router
from django.contrib.auth.hashers import make_password
from schemas import LoginSchema, RegisterSchema

auth_router = Router()
User = get_user_model()

@auth_router.post("/login", response=LoginSchema)
def login(request, user: LoginSchema):
    pass

@auth_router.post("/register")
def register(request, data: RegisterSchema):
    if User.objects.filter(username=data.email).exists():
        return {"error" : "Email already exists"}, 400
    
    user_model = User.objects.create(
        username=data.email, 
        password=make_password(data.password)
    )
    
    return user_model
    
