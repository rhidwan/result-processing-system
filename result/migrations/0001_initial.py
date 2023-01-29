# Generated by Django 3.2.12 on 2022-12-06 16:55

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('students', '0005_auto_20221129_1624'),
        ('committee', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Catm',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('attendance', models.FloatField()),
                ('ct_1', models.FloatField()),
                ('ct_2', models.FloatField()),
                ('ct_3', models.FloatField()),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='students.student')),
            ],
        ),
        migrations.CreateModel(
            name='Score',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('code_no', models.CharField(blank=True, max_length=20, null=True)),
                ('is_improvement', models.BooleanField(default=False)),
                ('section_a', models.FloatField(blank=True, null=True)),
                ('section_b', models.FloatField(blank=True, null=True)),
                ('final_exam_mark', models.FloatField(blank=True, null=True)),
                ('mark_obtained', models.FloatField(blank=True, null=True)),
                ('percentage', models.FloatField(blank=True, null=True)),
                ('letter_grade', models.CharField(blank=True, max_length=4, null=True)),
                ('grade_point', models.FloatField(blank=True, null=True)),
                ('approved_by', models.ManyToManyField(related_name='approved_by', to=settings.AUTH_USER_MODEL)),
                ('catm', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='result.catm')),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='committee.course')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='students.student')),
            ],
        ),
        migrations.AddConstraint(
            model_name='score',
            constraint=models.UniqueConstraint(fields=('course', 'code_no'), name='course_code_no_unique'),
        ),
    ]
