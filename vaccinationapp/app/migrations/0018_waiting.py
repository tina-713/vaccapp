# Generated by Django 3.2 on 2021-05-12 18:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0017_auto_20210512_1635'),
    ]

    operations = [
        migrations.CreateModel(
            name='Waiting',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('spot', models.PositiveIntegerField(default=0)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('office', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.office')),
                ('person', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.person')),
            ],
        ),
    ]