# Generated by Django 5.1.4 on 2024-12-11 12:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_ticket'),
    ]

    operations = [
        migrations.AddField(
            model_name='ticket',
            name='response',
            field=models.TextField(blank=True, null=True),
        ),
    ]
