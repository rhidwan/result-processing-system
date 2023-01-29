from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import ugettext_lazy as _

from .managers import UserManager


class User(AbstractUser):
    id = models.AutoField(primary_key=True)
    GENDER_CHOICES = [(0, 'Male'), (1, 'Female'), (2, 'Other')]

    username = None
    email = models.EmailField(_('email address'), unique=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ["full_name", "date_of_birth", "gender"]

    objects = UserManager()

    full_name = models.CharField(blank=True, max_length=100)
    date_of_birth = models.DateField(blank=True, null=True)
    gender = models.IntegerField(choices=GENDER_CHOICES)
    is_chairman = models.BooleanField(
            _('chairman status'),
            default=False,
            help_text=_('Designates whether the user is a Chairman Or not.'),
        )

    def __str__(self):
        return self.email

