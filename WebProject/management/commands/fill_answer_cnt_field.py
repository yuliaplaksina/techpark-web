from django.db import transaction
from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User
from WebProject.models import Question, Profile, Answer, Tag
from random import choice, randint


class Command(BaseCommand):

    @transaction.atomic()
    def handle(self, *args, **options):
        self.add_answer_cnt()

    def add_answer_cnt(self):
        questions = Question.objects.add_answer_count().all()

        for question in questions:

            question.answer_cnt = question.answer_count
            question.save()
