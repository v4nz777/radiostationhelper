# Generated by Django 4.0.2 on 2022-02-17 05:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0011_user_address_alter_user_facebook'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='mobile_number',
            field=models.CharField(blank=True, max_length=20),
        ),
        migrations.AlterField(
            model_name='user',
            name='tel_number',
            field=models.CharField(blank=True, max_length=20),
        ),
    ]
