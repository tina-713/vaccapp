# Generated by Django 3.2 on 2021-08-14 08:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0026_alter_appointment_time'),
    ]

    operations = [
        migrations.AddField(
            model_name='appointment',
            name='user',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='app.user'),
            preserve_default=False,
        ),
    ]