# Generated by Django 5.0.1 on 2024-08-22 14:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userauth', '0004_user_bio'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='is_vendor',
            field=models.BooleanField(default=False),
        ),
    ]
