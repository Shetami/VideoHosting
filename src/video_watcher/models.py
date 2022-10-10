from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.core.validators import FileExtensionValidator
from django.db import models


class Studio(models.Model):
    name = models.CharField("Name studio", max_length=128, unique=True)


class Timetable(models.Model):
    DAY_WEEK = (
        (1, 'Sunday'),
        (2, 'Monday'),
        (3, 'Tuesday'),
        (4, 'Wednesday'),
        (5, 'Thursday'),
        (6, 'Friday'),
        (7, 'Saturday'),
    )
    day_week_id = models.PositiveSmallIntegerField(choices=DAY_WEEK)


class Genres(models.Model):
    name = models.CharField("Genres", max_length=64, blank=True)

    def __str__(self):
        return self.name


class Serial(models.Model):
    DAY_WEEK = (
        (1, 'Sunday'),
        (2, 'Monday'),
        (3, 'Tuesday'),
        (4, 'Wednesday'),
        (5, 'Thursday'),
        (6, 'Friday'),
        (7, 'Saturday'),
        (8, 'Finished')
    )
    title = models.CharField("Title", max_length=128, unique=True)
    description = models.TextField("Description")
    image = models.ImageField("Image serial", upload_to="media/serialImage", blank=True,
                              validators=[FileExtensionValidator(['png', 'jpeg'])])
    rating_sum = models.FloatField(default=0.00)
    date = models.DateField("Date")
    episode_count = models.PositiveSmallIntegerField("Episode count")
    studio = models.ForeignKey(Studio, related_name="serial_studio", on_delete=models.CASCADE)
    day_week = models.PositiveSmallIntegerField(choices=DAY_WEEK)
    genres = models.ManyToManyField(Genres, verbose_name="Genres")

    def __str__(self):
        return self.title


class Video(models.Model):
    video = models.FileField("Video", upload_to="videos", blank=True)
    serials = models.ForeignKey(Serial, related_name="serial_video", on_delete=models.CASCADE)


