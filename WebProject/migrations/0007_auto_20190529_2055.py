# Generated by Django 2.1.7 on 2019-05-29 17:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('WebProject', '0006_question_answer_cnt'),
    ]

    operations = [
        migrations.CreateModel(
            name='AnswerLike',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('answer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='WebProject.Answer')),
                ('profile', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='WebProject.Profile')),
            ],
        ),
        migrations.CreateModel(
            name='QuestionLike',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('profile', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='WebProject.Profile')),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='WebProject.Question')),
            ],
        ),
        migrations.AddField(
            model_name='answer',
            name='likes',
            field=models.ManyToManyField(related_name='liked_answers', through='WebProject.AnswerLike', to='WebProject.Profile'),
        ),
        migrations.AddField(
            model_name='question',
            name='likes',
            field=models.ManyToManyField(related_name='liked_questions', through='WebProject.QuestionLike', to='WebProject.Profile'),
        ),
    ]