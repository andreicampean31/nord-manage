# Generated by Django 3.1.7 on 2021-08-13 15:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('defecte', '0003_auto_20210813_1454'),
    ]

    operations = [
        migrations.RenameField(
            model_name='temporary',
            old_name='action_performed',
            new_name='act_perf',
        ),
        migrations.RenameField(
            model_name='temporary',
            old_name='component_phase_reference',
            new_name='comp_ph_ref',
        ),
        migrations.RenameField(
            model_name='temporary',
            old_name='functional_test',
            new_name='func_test',
        ),
        migrations.RenameField(
            model_name='temporary',
            old_name='security_test',
            new_name='sec_test',
        ),
        migrations.RenameField(
            model_name='temporary',
            old_name='tip_componenta',
            new_name='tip_comp',
        ),
    ]
