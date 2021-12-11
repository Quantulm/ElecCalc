from django.db import models
from django.core.files.storage import FileSystemStorage

# Designation of file storage locations
fs = FileSystemStorage(location="data")


# Create your models here.


class LectureHall(models.Model):
    def __str__(self):
        return self.hall_name

    def get_base_consumption():
        """Calculates basic consumption without students"""

        self.base_consumption = (
            self.light_blackboard_count * self.light_blackboard_consumption
            + self.light_stairs_count * self.light_stairs_consumption
            + self.beamer_count * self.beamer_consumption
            + self.amplifier_count * self.amplifier_consumption
            + self.mic_count * self.mic_consumption
            + self.cam_count * self.cam_consumption
            + self.other
        )

        return self.base_consumption

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
    beamer_count = models.PositiveIntegerField("Beamer - Number of beamers")
    beamer_power = models.FloatField("Beamer - Power per beamer (W)")
    beamer_consumption = models.FloatField(
        "Beamer - Consumption per beamer per hour (kWh/h)"
    )
    amplifier_count = models.PositiveIntegerField("Amplifier - Number of amplifiers")
    amplifier_power = models.FloatField("Amplifier - Power per amplifier (W)")
    amplifier_consumption = models.FloatField(
        "Amplifier - Consumption per amplifier per hour (kWh/h)"
    )
    mic_count = models.PositiveIntegerField("Microphone - Number of microphones")
    mic_power = models.FloatField("Microphone - Power per microphone (W)")
    mic_consumption = models.FloatField(
        "Microphone - Consumption per microphone per hour (kWh/h)"
    )
    cam_count = models.PositiveIntegerField("Camera - Number of cameras")
    cam_power = models.FloatField("Camera - Power per camera (W)")
    cam_consumption = models.FloatField(
        "Camera - Consumption per camera per hour (kWh/h)"
    )
    other = models.FloatField("Other energy consuming sources (kWh/h)")


class Streaming(models.Model):
    def __str__(self):
        return self.streaming_name

    streaming_name = models.CharField("Name of the streaming service", max_length=200)
    streaming_access_power = models.FloatField("Access - Power (W)")
    streaming_access_consumption = models.FloatField(
        "Access - Consumption per hour (kWh/h)"
    )
    streaming_router_power = models.FloatField("Router - Power (W)")
    streaming_router_consumption = models.FloatField(
        "Router - Consumption per hour (kWh/h)"
    )
    streaming_core_pergb = models.FloatField(
        "Core network - Energy consumption per GB data consumption (kWh/GB)"
    )
    streaming_core_data = models.FloatField(
        "Core network - Data consumption per hour (GB/h)"
    )


class Video_On_Demand(models.Model):
    def __str__(self):
        return self.vod_name

    vod_name = models.CharField("Name of the VoD service", max_length=200)
    vod_access_power = models.FloatField("Access - Power (W)")
    vod_access_consumption = models.FloatField("Access - Consumption per hour (kWh/h)")
    vod_router_power = models.FloatField("Router - Power (W)")
    vod_router_consumption = models.FloatField("Router - Consumption per hour (kWh/h)")
    vod_core_pergb = models.FloatField(
        "Core network - Energy consumption per GB data consumption (kWh/GB)"
    )
    vod_core_data = models.FloatField("Core network - Data consumption per hour (GB/h)")
    vod_data_center_power = models.FloatField(
        "Data center - Power per TB data consumption (W/TB)"
    )
    vod_data_center_data = models.FloatField(
        "Data center - Data consumption per hour (TB/h)"
    )
    vod_data_center_consumption = models.FloatField(
        "Data center - Energy consumption per hour (kWh/h)"
    )


class Living_Situation(models.Model):
    def __str__(self):
        return self.living_name

    living_name = models.CharField("Name of the living situation", max_length=200)
    living_num_lights = models.PositiveIntegerField(
        "Number of light bulbs in the study area"
    )
    living_power = models.FloatField("Average power per light bulb (W)")
    living_consumption = models.FloatField(
        "Energy consumption per light bulb per hour (kWh/h)"
    )


class Electronic_Device(models.Model):
    def __str__(self):
        return self.device_name

    device_name = models.CharField("Name of the electronic device", max_length=200)
    device_power = models.FloatField("Power of the device (W)")
    davice_consumption = models.FloatField("Energy consumption of the device (kWh)")


class Transportation(models.Model):
    def __str__(self):
        return self.transport_name

    transport_name = models.CharField("Name of means of transportation", max_length=200)
    transport_conv_fact = models.FloatField(
        "Conversion factor from CO_2 emitted to energy consumed (kWh/kg)"
    )
    transport_dist = models.FloatField(
        "Conversion factor from minutes travelled to kilometers traveled (km/min)"
    )
    trasport_consumption = models.FloatField("Energy consumption per distance (kWh/km)")


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
    stdev_travel_distance = models.FloatField(
        "Standard deviation of average travel distance of students"
    )


class Survey(models.Model):
    def __str__(self):
        return self.survey_name

    survey_name = models.CharField("Survey name", max_length=200)
    survey_file = models.FileField(upload_to="data")
