from django.db import models
from django.core.files.storage import FileSystemStorage

# Designation of file storage locations
fs = FileSystemStorage(location='data')


# Create your models here.



class LectureHall(models.Model):
    def __str__(self):
        return self.hall_name

    hall_name = models.CharField("Name of the lecture hall", max_length=200)
    seating_capacity = models.PositiveIntegerField("Number of available seats")
    seating_capacity_distancing = models.PositiveIntegerField(
            "Number of available seats with social distancing",
        )
    light_blackboard_count = models.PositiveIntegerField(
            "Light bulbs: Blackboard - Number of light bulbs",
        )
    light_blackboard_power = models.FloatField(
            "Light bulbs: Blackboard - Power per light bulb (W)",
        )
    light_blacboard_consumption = models.FloatField(
            "Light bulbs: Blackboard - Average consumption per light bulb (kWh/h)"
        )
    light_stairs_count = models.PositiveIntegerField(
            "Light bulbs: Stairs - Number of light bulbs",
        )
    light_stairs_power = models.FloatField(
            "Light bulbs: Stairs - Power per light bulb (W)",
        )
    light_stairs_consumption = models.FloatField(
            "Light bulbs: Stairs - Average consumption per light bulb per hour (kWh/h)"
        )
    beamer_count = models.PositiveIntegerField(
            "Beamer - Number of beamers"
        )
    beamer_power = models.FloatField(
            "Beamer - Power per beamer (W)"
        )
    beamer_consumption = models.FloatField(
            "Beamer - Consumption per beamer per hour (kWh/h)"
        )
    amplifier_count = models.PositiveIntegerField(
            "Amplifier - Number of amplifiers"
        )
    amplifier_power = models.FloatField(
            "Amplifier - Power per amplifier (W)"
        )
    amplifier_consumption = models.FloatField(
            "Amplifier - Consumption per amplifier per hour (kWh/h)"
        )
    mic_count = models.PositiveIntegerField(
            "Microphone - Number of microphones"
        )
    mic_power = models.FloatField(
            "Microphone - Power per microphone (W)"
        )
    mic_consumption = models.FloatField(
            "Microphone - Consumption per microphone per hour (kWh/h)"
        )
    cam_count = models.PositiveIntegerField(
            "Camera - Number of cameras"
        )
    cam_power = models.FloatField(
            "Camera - Power per camera (W)"
        )
    cam_consumption = models.FloatField(
            "Camera - Consumption per camera per hour (kWh/h)"
        )
    other = models.FloatField(
            "Other energy consuming sources (kWh/h)"
        )






class Faculty(models.Model):
    def __str__(self):
        return self.faculty_name

    faculty_name = models.CharField("Faculty name", max_length=200)
    lec_length = models.IntegerField("Average lecture length (min)")
    dev_usage = models.FloatField("Usage of electronic devices (%)")


class University(models.Model):
    def __str__(self):
        return self.university_name

    university_name = models.CharField("Name of the University/Campus", max_length=200)
    avg_travel_distance = models.FloatField("Average travel distance of students")
    stdev_travel_distance = models.FloatField("Standard deviation of average travel distance of students")


class Device(models.Model):
    def __str__(self):
        return self.device_name

    device_name = models.CharField("Device name", max_length=200)
    power_consumption_online = models.FloatField("Power consumption during online lecture")
    power_consumption_offline = models.FloatField("Power consumption during onsite lecture")


class Survey(models.Model):
    def __str__(self):
        return self.survey_name

    survey_name = models.CharField("Survey name", max_length=200)
    survey_file = models.FileField(upload_to="data")
