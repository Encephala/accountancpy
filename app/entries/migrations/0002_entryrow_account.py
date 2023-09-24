# Generated by Django 4.2.4 on 2023-09-24 17:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
        ('entries', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='entryrow',
            name='account',
            field=models.ForeignKey(blank=True, default='acc1', on_delete=django.db.models.deletion.PROTECT, to='accounts.account'),
            preserve_default=False,
        ),
    ]
