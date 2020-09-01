# Generated by Django 2.1.15 on 2020-08-31 06:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_auto_20200830_1827'),
    ]

    operations = [
        migrations.AddField(
            model_name='process',
            name='is_megaprocess',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='process',
            name='parent',
            field=models.ForeignKey(blank=True, limit_choices_to={'is_megaprocess': True}, null=True, on_delete=django.db.models.deletion.SET_NULL, to='core.Process'),
        ),
        migrations.AlterField(
            model_name='orgunit',
            name='acronym',
            field=models.CharField(max_length=3, null=True),
        ),
    ]
