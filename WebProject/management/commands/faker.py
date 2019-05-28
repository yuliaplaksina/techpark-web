from django.db import transaction
from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User
from WebProject.models import Question, Profile, Answer, Tag
from faker import Faker
from random import choice, randint


fake = Faker()


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('--question', type=int)
        parser.add_argument('--user', type=int)
        parser.add_argument('--answer', type=int)
        parser.add_argument('--tag', type=int)
        parser.add_argument('--qsttag', type=int)

    @transaction.atomic()
    def handle(self, *args, **options):
        users_cnt = options['user']
        questions_cnt = options['question']
        answers_cnt = options['answer']
        tags_cnt = options['tag']
        qst_tag_cnt = options['qsttag']

        if tags_cnt is not None:
            self.generate_tags(tags_cnt)

        if users_cnt is not None:
            self.generate_users(users_cnt)

        if answers_cnt is not None:
            self.generate_answers(answers_cnt)

        if questions_cnt is not None:
            self.generate_questions(questions_cnt)

        if qst_tag_cnt is not None:
            self.generate_qst_tag(qst_tag_cnt)

    def generate_tags(self, tags_cnt):
        print(f"GENERATE TAGS {tags_cnt}")

        text_file = open("some_more_files/google-10000-english.txt", "r")
        tags = text_file.readlines()

        for i in range(tags_cnt):
            Tag.objects.create(
                name=tags[i]
            )

    def generate_users(self, users_cnt):
        print(f"GENERATING USERS {users_cnt}")
        text_file = open("some_more_files/10000-user-name.txt", "r")
        user_names = text_file.readlines()

        for i in range(users_cnt):
            usr = User.objects.create_user(
                user_names[i],
                email=fake.email(),
                password='passworduser',

            )

            Profile.objects.create(
                user=usr,
                rating=randint(0, 100)
            )

        print(f"HAVE BEEN GENERATED USERS {users_cnt}")

    def generate_questions(self, questions_cnt):
        print(f"GENERATE QUESTIONS {questions_cnt}")
        uids = list(Profile.objects.values_list('id', flat=True))

        for i in range(questions_cnt):
            Question.objects.create(
                author_id=choice(uids),
                title=fake.sentence(),
                text='\n'.join(fake.sentences(fake.random_int(2, 8))),
                rating=randint(0, 100),
                data_added=fake.date(pattern="%Y-%m-%d", end_datetime=None)
            )

    def generate_qst_tag(self, qst_tag_cnt):
        for i in range(qst_tag_cnt):
            for j in range(3):
                tid = randint(1, 10000)
                tag = Tag.objects.get(id=tid)
                qst = Question.objects.get(id=i+200006)
                qst.tags.add(tag)

    def generate_answers(self, answers_cnt):
        print(f"GENERATE QUESTIONS {answers_cnt}")
        uids = list(Profile.objects.values_list('id', flat=True))
        aids = list(Question.objects.values_list('id', flat=True))
        for i in aids:
            answers_col = randint(5, 20)

            for j in range(answers_col):
                Answer.objects.create(
                    author_id=choice(uids),
                    text='\n'.join(fake.sentences(fake.random_int(1, 3))),
                    rating=randint(0, 10),
                    data_added=fake.date(pattern="%Y-%m-%d", end_datetime=None),
                    question_id=i
                )
