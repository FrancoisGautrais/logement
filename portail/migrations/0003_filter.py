# Generated by Django 4.0.3 on 2022-04-09 12:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('portail', '0002_annonce_custom_id_annonce_disable_alter_annonce_id'),
    ]

    operations = [
        migrations.CreateModel(
            name='Filter',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.TextField()),
                ('type', models.TextField()),
                ('score', models.IntegerField(default=1)),
            ],
        ),
    ]
