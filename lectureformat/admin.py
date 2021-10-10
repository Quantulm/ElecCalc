from django.contrib import admin

# Register your models here.
from .models import LectureHall
from .models import Faculty
from .models import Device
from .models import University
from .models import Survey

admin.site.register(LectureHall)
admin.site.register(Faculty)
admin.site.register(Device)
admin.site.register(University)
admin.site.register(Survey)