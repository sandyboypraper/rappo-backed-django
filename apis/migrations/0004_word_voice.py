# Generated by Django 3.1.7 on 2021-03-12 20:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('apis', '0003_auto_20210312_2042'),
    ]

    operations = [
        migrations.AddField(
            model_name='word',
            name='voice',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='apis.voice'),
        ),
    ]