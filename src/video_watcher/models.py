from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.core.validators import FileExtensionValidator
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils import timezone


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
    rating_sum = models.DecimalField(max_digits=2, decimal_places=2, default=0.00)
    date = models.DateField("Date")
    episode_count = models.PositiveSmallIntegerField("Episode count")
    studio = models.ForeignKey(Studio, related_name="serial_studio", on_delete=models.CASCADE)
    day_week = models.PositiveSmallIntegerField(choices=DAY_WEEK)
    genres = models.ManyToManyField(Genres, verbose_name="Genres")

    def get_rating_sum(self):
        pass

    def __str__(self):
        return self.title


class Video(models.Model):
    video = models.FileField("Video", upload_to="videos", blank=True),
    serials = models.ForeignKey(Serial, related_name="serial_video", on_delete=models.CASCADE)


class CustomAccountManager(BaseUserManager):

    def create_superuser(self, email, username, password, **kwargs):
        kwargs.setdefault('is_staff', True)
        kwargs.setdefault('is_superuser', True)
        kwargs.setdefault('is_active', True)
        if kwargs.get('is_staff') is not True:
            raise ValueError('Superuser must be assigned to is_staff=True')
        if kwargs.get('is_superuser') is not True:
            raise ValueError('Superuser must be assigned to is_superuser=True')

        return self.create_user(email, username, password, **kwargs)

    def create_user(self, email, username, password, **kwargs):
        if not email:
            raise ValueError(_('You must provide an email address'))
        email = self.normalize_email(email)
        user = self.model(email=email, username=username, **kwargs)
        user.set_password(password)
        user.save()
        return user


class User(AbstractBaseUser, PermissionsMixin):
    username_validator = UnicodeUsernameValidator()
    username = models.CharField(
        _("username"),
        max_length=150,
        unique=True,
        help_text=_(
            "Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only."
        ),
        validators=[username_validator],
        error_messages={
            "unique": _("A user with that username already exists."),
        },
    )
    image = models.ImageField("Image user", upload_to="media/userImage", blank=True)
    email = models.EmailField(_("email address"), blank=True)
    is_staff = models.BooleanField(
        _("staff status"),
        default=False,
        help_text=_("Designates whether the user can log into this admin site."),
    )
    is_active = models.BooleanField(
        _("active"),
        default=True,
        help_text=_(
            "Designates whether this user should be treated as active. "
            "Unselect this instead of deleting accounts."
        ),
    )
    date_joined = models.DateTimeField(_("date joined"), default=timezone.now)

    objects = CustomAccountManager()

    EMAIL_FIELD = "email"
    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["email"]

    class Meta:
        verbose_name = _("user")
        verbose_name_plural = _("users")

    planned = models.ManyToManyField(Serial, verbose_name="Planned", related_name="planned", blank=True)
    watching = models.ManyToManyField(Serial, verbose_name="Watching", related_name="watching", blank=True)
    finished = models.ManyToManyField(Serial, verbose_name="Finished", related_name="finished", blank=True)

    def __str__(self):
        return self.username


class Review(models.Model):
    text = models.TextField("Text review", max_length=1024)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    serial = models.OneToOneField(Serial, on_delete=models.CASCADE)


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
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    serial = models.ForeignKey(Serial, on_delete=models.CASCADE)
    rate = models.PositiveSmallIntegerField(choices=RATING_CHOICES)
