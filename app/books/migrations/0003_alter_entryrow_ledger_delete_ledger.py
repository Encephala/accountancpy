# Generated by Django 4.2.4 on 2023-09-12 20:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ledgers', '0001_initial'),
        ('books', '0002_entry_entryrow_journal_remove_entriesrow_entry_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='entryrow',
            name='ledger',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='ledgers.ledger'),
        ),
        migrations.DeleteModel(
            name='Ledger',
        ),
    ]