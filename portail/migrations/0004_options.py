# Generated by Django 4.0.3 on 2022-04-11 17:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('portail', '0003_filter'),
    ]

    operations = [
        migrations.CreateModel(
            name='Options',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('key', models.TextField(unique=True)),
                ('value', models.TextField()),
            ],
        ),
    ]
