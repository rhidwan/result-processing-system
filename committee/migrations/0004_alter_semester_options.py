# Generated by Django 3.2.12 on 2022-12-16 17:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('committee', '0003_auto_20221216_0809'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='semester',
            options={'ordering': ('-academic_year', 'name')},
        ),
    ]