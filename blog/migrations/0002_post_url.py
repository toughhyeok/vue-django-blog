# Generated by Django 3.2.15 on 2022-09-26 22:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='url',
            field=models.URLField(null=True, verbose_name='URL'),
        ),
    ]
