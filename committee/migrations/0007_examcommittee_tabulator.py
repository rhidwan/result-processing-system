# Generated by Django 3.2.12 on 2023-02-01 17:29

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('committee', '0006_course_course_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='examcommittee',
            name='tabulator',
            field=models.ManyToManyField(related_name='tabulator', to=settings.AUTH_USER_MODEL),
        ),
    ]
