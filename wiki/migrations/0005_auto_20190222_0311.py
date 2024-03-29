# Generated by Django 2.1.7 on 2019-02-22 03:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wiki', '0004_auto_20190221_2246'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='article',
            options={'ordering': ['-id']},
        ),
        migrations.AlterModelOptions(
            name='discussion',
            options={'ordering': ['-id']},
        ),
        migrations.AddField(
            model_name='article',
            name='rate_count',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='article',
            name='rate_total',
            field=models.IntegerField(default=0),
        ),
    ]
