# Generated by Django 3.2.12 on 2023-04-05 20:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('result', '0012_score_is_improved'),
    ]

    operations = [
        migrations.AddField(
            model_name='catm',
            name='ct_4',
            field=models.FloatField(blank=True, null=True),
        ),
    ]