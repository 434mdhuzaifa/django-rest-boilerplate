# Generated by Django 5.0 on 2024-10-11 06:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userAuth', '0003_alter_resettoken_created_at'),
    ]

    operations = [
        migrations.AddField(
            model_name='resettoken',
            name='isvalid',
            field=models.BooleanField(default=True),
        ),
    ]
