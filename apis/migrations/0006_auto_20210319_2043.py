# Generated by Django 3.1.7 on 2021-03-19 20:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('apis', '0005_auto_20210315_1848'),
    ]

    operations = [
        migrations.AlterField(
            model_name='word',
            name='voice',
            field=models.ForeignKey(default=1, null=True, on_delete=django.db.models.deletion.SET_NULL, to='apis.voice'),
        ),
    ]
