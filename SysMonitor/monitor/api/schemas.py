from ninja import ModelSchema, Schema
from monitor.models import InputActivity

class InputActivitySchema(ModelSchema):
    class Config:
        model = InputActivity
        model_fields = ['timestamp', 'keyboard_activity', 'mouse_activity']

class InputActivityCreateSchema(Schema):
    keyboard_activity: int = 0  
    mouse_activity: int = 0   
