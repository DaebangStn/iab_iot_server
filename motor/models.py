from django.db import models
from django.utils import timezone


class Mode(models.IntegerChoices):
    OFF = 0
    ON = 1
    ERR = 2
    DISCON = 3


class Controller(models.Model):
    mac = models.CharField(primary_key=True, max_length=12)
    speed_data = models.IntegerField(default=0)
    speed_target = models.IntegerField(default=0)
    duty = models.IntegerField(default=0)
    mode = models.IntegerField(default=Mode.DISCON, choices=Mode.choices)
    updated_last = models.DateTimeField('date updated')
    controlled_last = models.DateTimeField('controlled updated')

    def __str__(self):
        return self.mac

    @classmethod
    def register(cls, mac):
        controller = cls(mac=mac, controlled_last=timezone.now(), updated_last=timezone.now())
        return controller


class Data(models.Model):
    mac = models.CharField(max_length=12)
    speed = models.IntegerField(default=0)
    duty = models.IntegerField(default=0)
    data_time = models.DateTimeField('date updated')

    def __str__(self):
        return str(self.id)

    @classmethod
    def register(cls, mac, speed, duty, data_time):
        data = cls(mac=mac, speed=speed, duty=duty, data_time=data_time)
        return data
