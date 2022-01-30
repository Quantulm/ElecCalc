from django.contrib import admin

# Register your models here.
from .models import LectureHall
from .models import StreamingService
from .models import VideoOnDemandService
from .models import LivingSituation
from .models import ElectronicDevice
from .models import Transportation
from .models import Faculty
from .models import University

admin.site.register(LectureHall)
admin.site.register(StreamingService)
admin.site.register(VideoOnDemandService)
admin.site.register(LivingSituation)
admin.site.register(ElectronicDevice)
admin.site.register(Transportation)
admin.site.register(Faculty)
admin.site.register(University)
