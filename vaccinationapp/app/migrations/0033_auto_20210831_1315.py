# Generated by Django 3.2 on 2021-08-31 13:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0032_alter_appointment_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='city',
            name='latitude',
            field=models.FloatField(default=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='city',
            name='longitude',
            field=models.FloatField(default=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='city',
            name='region',
            field=models.CharField(default=1, max_length=64),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='city',
            name='siruta',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='county',
            name='code',
            field=models.CharField(default=1, max_length=2),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='county',
            name='created_at',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
