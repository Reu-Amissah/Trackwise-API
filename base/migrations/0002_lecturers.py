# Generated by Django 4.2.3 on 2023-07-27 13:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Lecturers',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('lecturerId', models.CharField(max_length=10, unique=True)),
                ('lecturerName', models.CharField(max_length=100)),
                ('password', models.CharField(max_length=128)),
            ],
        ),
    ]
