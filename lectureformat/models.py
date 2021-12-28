from django.db import models
from django.core.files.storage import FileSystemStorage

# Designation of file storage locations
fs = FileSystemStorage(location="data")


# Create your models here.


class LectureHall(models.Model):
    def __str__(self):
        return self.hall_name

    # TODO get & set attribute function

    def get_consumption(self, time):
        """
        Calculates basic consumption without students
        ------
        Parameters
        time : float
            Duration of the lecture

        ------
        Return :
        consumption : float
            returns consumption in kWh
        """

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
    seating_capacity_distancing = models.PositiveIntegerField("Number of available seats with social distancing")

    light_blackboard_count = models.PositiveIntegerField("Light bulbs: Blackboard - Number of light bulbs")
    light_blackboard_power = models.FloatField("Light bulbs: Blackboard - Power per light bulb (W)")

    light_stairs_count = models.PositiveIntegerField("Light bulbs: Stairs - Number of light bulbs")
    light_stairs_power = models.FloatField("Light bulbs: Stairs - Power per light bulb (W)")

    beamer_count = models.PositiveIntegerField("Beamer - Number of beamers")
    beamer_power = models.FloatField("Beamer - Power per beamer (W)")

    amplifier_count = models.PositiveIntegerField("Amplifier - Number of amplifiers")
    amplifier_power = models.FloatField("Amplifier - Power per amplifier (W)")

    mic_count = models.PositiveIntegerField("Microphone - Number of microphones")
    mic_power = models.FloatField("Microphone - Power per microphone (W)")

    cam_count = models.PositiveIntegerField("Camera - Number of cameras")
    cam_power = models.FloatField("Camera - Power per camera (W)")

    other = models.FloatField("Other energy consuming sources (kWh/h)")


class StreamingService(models.Model):
    def __str__(self):
        return self.streaming_name

    def get_consumption(self):
        return 8000

    streaming_name = models.CharField("Name of the streaming service", max_length=200)
    streaming_access_power = models.FloatField("Access - Power (W)")
    streaming_router_power = models.FloatField("Router - Power (W)")
    streaming_core_pergb = models.FloatField("Core network - Energy consumption per GB data consumption (kWh/GB)")
    streaming_core_data = models.FloatField("Core network - Data consumption per hour (GB/h)")


class VideoOnDemandService(models.Model):
    def __str__(self):
        return self.vod_name

    def get_consumption(self):
        return 8000

    vod_name = models.CharField("Name of the VoD service", max_length=200)
    vod_access_power = models.FloatField("Access - Power (W)")
    vod_router_power = models.FloatField("Router - Power (W)")
    vod_core_pergb = models.FloatField("Core network - Energy consumption per GB data consumption (kWh/GB)")
    vod_core_data = models.FloatField("Core network - Data consumption per hour (GB/h)")
    vod_data_center_power = models.FloatField("Data center - Power per TB data consumption (W/TB)")
    vod_data_center_data = models.FloatField("Data center - Data consumption per hour (TB/h)")



class Living_Situation(models.Model):
    def __str__(self):
        return self.living_name

    def get_consumption(self):
        return 8000

    living_name = models.CharField("Name of the living situation", max_length=200)
    living_num_lights = models.PositiveIntegerField("Number of light bulbs in the study area")
    living_power = models.FloatField("Average power per light bulb (W)")



class Electronic_Device(models.Model):
    def __str__(self):
        return self.device_name

    def get_consumption(self):
        return 8000

    device_name = models.CharField("Name of the electronic device", max_length=200)
    device_power = models.FloatField("Power of the device (W)")



class Transportation(models.Model):
    def __str__(self):
        return self.transport_name

    def get_consumption(self):
        return 8000

    transport_name = models.CharField("Name of means of transportation", max_length=200)
    transport_name_file = models.FileField(upload_to="data")

    transport_conv_fact = models.FloatField("Conversion factor from CO_2 emitted to energy consumed (kWh/kg)")
    transport_dist = models.FloatField("Conversion factor from minutes travelled to kilometers traveled (km/min)")
    transport_consumption = models.FloatField("Energy consumption per distance (kWh/km)")

'Suggest/TODO: This can be the child class of all university and parent class of the others'
class Faculty(models.Model):
    def __str__(self):
        return self.faculty_name

    def get_consumption(self):
        return 8000

    faculty_name = models.CharField("Faculty name", max_length=200)

    lecture_frequency = models.FloatField("Number of lectures attended on daily average by faculty")
    lecture_freq_file = models.FileField(upload_to="data", blank=True)

    online_lec_freq = models.FloatField("Hours per day of watching online lectures")
    online_lec_file = models.FileField(upload_to="data",blank=True)

    live_lec = models.FloatField("Percentage of online lectured watched live per faculty")
    live_lec_file = models.FileField(upload_to="data",blank=True)

    lec_length = models.IntegerField("Average lecture length (min) per faculty")
    dev_usage = models.FloatField("Usage of electronic devices (%) per faculty",blank=True)

    elec_dev_use = models.FloatField("Use of electronic device by faculty")
    elec_dev_use_file = models.FileField(upload_to="data",blank=True)

    elec_dev_freq = models.FloatField("frequency of use of electronic devices by faculty")
    elec_dev_freq_file = models.FileField(upload_to="data",blank=True)

    elec_dev_type = models.CharField("Device type by faculty", max_length=200)
    elec_dev_type_file = models.FileField(upload_to="data",blank=True)

'Suggest/TODO: This can be the parent class of all the previous ones'
class University(models.Model):
    def __str__(self):
        return self.university_name

    def get_consumption(self):
        return 8000

    university_name = models.CharField("Name of the University/Campus", max_length=200)
    avg_travel_distance = models.FloatField("Average travel distance of students")
    stdev_travel_distance = models.FloatField("Standard deviation of average travel distance of students")

    transport_duration = models.FloatField("Time spent to or from university")
    transport_dur_file= models.FileField(upload_to="data",blank=True)

    transport_frequency = models.FloatField("Transport frequency in days per week")
    transport_freq_file= models.FileField(upload_to="data",blank=True)
