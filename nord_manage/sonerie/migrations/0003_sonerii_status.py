# Generated by Django 3.1.7 on 2021-09-04 15:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sonerie', '0002_auto_20210904_1457'),
    ]

    operations = [
        migrations.AddField(
            model_name='sonerii',
            name='status',
            field=models.BooleanField(default=1),
            preserve_default=False,
        ),
    ]
