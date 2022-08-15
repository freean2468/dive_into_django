# Generated by Django 3.2.15 on 2022-08-15 04:56

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=64, unique=True, verbose_name='Email')),
                ('nickname', models.CharField(max_length=16, unique=True, verbose_name='Nickname')),
                ('password', models.CharField(max_length=128, verbose_name='Password')),
                ('name', models.CharField(max_length=32, verbose_name='Name')),
                ('phone', models.CharField(max_length=11, unique=True, verbose_name='Phone')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
    ]
