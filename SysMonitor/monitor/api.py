from ninja import NinjaAPI
from .models import InputActivity
from .schemas import InputActivitySchema, InputActivityCreateSchema
from django.shortcuts import get_object_or_404

api = NinjaAPI()

@api.get("/input_activity", response=list[InputActivitySchema])
def get_input_activities(request):
    return InputActivity.objects.all()

@api.get("/input_activity/{timestamp}", response=InputActivitySchema)
def get_input_activity(request, timestamp: str):
    activity = get_object_or_404(InputActivity, timestamp=timestamp)
    return activity

@api.post("/input_activity", response=InputActivitySchema)
def create_input_activity(request, input_activity: InputActivityCreateSchema):
    input_activity_data = input_activity.dict()
    input_activity_model = InputActivity.objects.create(**input_activity_data)
    return input_activity_model
