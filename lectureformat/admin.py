from django.contrib import admin

# Register your models here.
from .models import LectureHall
from .models import Streaming
from .models import Video_On_Demand
from .models import Living_Situation
from .models import Electronic_Device
from .models import Transportation
from .models import Faculty
from .models import University
from .models import Survey

admin.site.register(LectureHall)
admin.site.register(Streaming)
admin.site.register(Video_On_Demand)
admin.site.register(Living_Situation)
admin.site.register(Electronic_Device)
admin.site.register(Transportation)
admin.site.register(Faculty)
admin.site.register(University)
admin.site.register(Survey)
