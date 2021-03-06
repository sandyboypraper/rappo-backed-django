# Generated by Django 3.1.7 on 2021-09-06 20:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('apis', '0010_auto_20210808_1953'),
    ]

    operations = [
        migrations.AlterField(
            model_name='voice',
            name='v_title',
            field=models.CharField(max_length=50, unique=True),
        ),
        migrations.RemoveField(
            model_name='word',
            name='category',
        ),
        migrations.AddField(
            model_name='word',
            name='category',
            field=models.ManyToManyField(to='apis.Category'),
        ),
        migrations.AlterField(
            model_name='word',
            name='titles_algo',
            field=models.CharField(max_length=300, unique=True),
        ),
    ]
