from django.db import models
from django.db.models import Sum

from src.auth_app.models.user_models import User
from src.video_watcher.models import Serial


class Review(models.Model):
    text = models.TextField("Text review", max_length=1024)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user")
    serial = models.ForeignKey(Serial, on_delete=models.CASCADE, related_name="reviews")
    parent = models.ForeignKey(
        'self', verbose_name="Parent", on_delete=models.SET_NULL, blank=True, null=True
    )

    def __str__(self):
        return f"{self.user.username} - {self.serial.title}"


class Rating(models.Model):
    RATING_CHOICES = (
        (1, "1"),
        (2, "2"),
        (3, "3"),
        (4, "4"),
        (5, "5"),
        (6, "6"),
        (7, "7"),
        (8, "8"),
        (9, "9"),
        (10, "10")
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="rating_user")
    serial = models.ForeignKey(Serial, on_delete=models.CASCADE, related_name="rating")
    rate = models.PositiveSmallIntegerField(choices=RATING_CHOICES)

    def get_rating_sum(self, pk):
        rating_count = self.objects.filter(serial=pk).count()
        rating_sum = self.objects.filter(serial=pk).aggregate(Sum('rate'))
        result = rating_sum['rate__sum']/rating_count
        return result

    def __str__(self):
        return f"{self.user.username} - {self.serial.title} - {self.rate}"
