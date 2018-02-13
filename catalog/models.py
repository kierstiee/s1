from django.db import models
from django.db.models.fields import DateTimeField

class Rental(models):
    create_date = DateTimeField.auto_now_add
    edit_date = DateTimeField.auto_now
