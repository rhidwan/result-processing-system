# Generated by Django 3.2.12 on 2022-12-06 16:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('students', '0005_auto_20221129_1624'),
        ('result', '0002_remove_catm_student'),
    ]

    operations = [
        migrations.AddField(
            model_name='catm',
            name='student',
            field=models.ForeignKey(default=18702015, on_delete=django.db.models.deletion.CASCADE, to='students.student'),
            preserve_default=False,
        ),
    ]
