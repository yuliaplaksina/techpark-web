# Generated by Django 2.1.7 on 2019-05-24 15:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('WebProject', '0002_answer_question'),
    ]

    operations = [
        migrations.AlterField(
            model_name='answer',
            name='rating',
            field=models.IntegerField(default=0, verbose_name='Рейтинг'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='rating',
            field=models.IntegerField(default=0, verbose_name='Рейтинг'),
        ),
    ]
