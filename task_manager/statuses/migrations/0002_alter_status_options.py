# Generated by Django 4.1.7 on 2023-03-08 17:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('statuses', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='status',
            options={'ordering': ['id'], 'verbose_name': 'status'},
        ),
    ]
