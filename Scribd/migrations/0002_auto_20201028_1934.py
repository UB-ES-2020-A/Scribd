# Generated by Django 3.1.2 on 2020-10-28 19:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Scribd', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='email',
            field=models.EmailField(max_length=254, unique=True),
        ),
    ]
