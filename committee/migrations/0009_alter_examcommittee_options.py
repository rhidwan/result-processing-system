# Generated by Django 3.2.12 on 2023-02-04 10:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('committee', '0008_alter_examcommittee_semester'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='examcommittee',
            options={'ordering': ('-academic_year',)},
        ),
    ]