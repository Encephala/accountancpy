# Generated by Django 4.2.4 on 2023-12-24 23:25

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('entries', '0007_alter_entryrow_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='entryrow',
            name='date',
            field=models.DateField(default=datetime.date.today),
        ),
    ]
