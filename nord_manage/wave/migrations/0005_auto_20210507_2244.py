# Generated by Django 3.1.7 on 2021-05-07 19:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wave', '0004_auto_20210507_2243'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productie',
            name='data',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
