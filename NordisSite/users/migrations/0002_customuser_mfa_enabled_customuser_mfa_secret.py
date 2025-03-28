# Generated by Django 5.1.6 on 2025-02-28 04:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='mfa_enabled',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='customuser',
            name='mfa_secret',
            field=models.CharField(blank=True, max_length=32, null=True),
        ),
    ]
