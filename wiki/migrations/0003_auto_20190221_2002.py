# Generated by Django 2.1.7 on 2019-02-21 20:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wiki', '0002_auto_20190221_1923'),
    ]

    operations = [
        migrations.AlterField(
            model_name='discussion',
            name='body',
            field=models.TextField(max_length=2000),
        ),
    ]
