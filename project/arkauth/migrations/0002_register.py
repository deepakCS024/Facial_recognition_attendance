# Generated by Django 3.0.14 on 2021-07-19 12:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('arkauth', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Register',
            fields=[
                ('sno', models.AutoField(primary_key=True, serialize=False)),
                ('usn', models.CharField(max_length=100)),
                ('gender', models.CharField(max_length=150)),
                ('sem', models.EmailField(max_length=254)),
                ('ia', models.CharField(max_length=55)),
                ('marks', models.CharField(max_length=55)),
                ('subject', models.CharField(max_length=100)),
            ],
        ),
    ]