# Generated by Django 3.2.12 on 2023-02-04 09:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('students', '0005_auto_20221129_1624'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='student',
            options={'ordering': ('student_id', 'session')},
        ),
    ]
