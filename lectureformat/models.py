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
    air_conditioning = models.BooleanField("Air conditioning available", default=True)
    beamer_power = models.FloatField("Power consumption of beamer (W)")
    light_count = models.PositiveIntegerField("Number of available lights")
    light_power = models.FloatField("Power consumption of a single light (W)")


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
