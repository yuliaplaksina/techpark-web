from django import forms
from django.db import transaction
from WebProject.models import Profile, Question, Tag, Answer
from django.contrib.auth.models import User


class RegisterForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password']
        widgets = {'password': forms.PasswordInput, 'email': forms.EmailInput}

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(user.password)

        print(user.password)

        if commit:
            with transaction.atomic():
                user.save()
                Profile.objects.create(user=user)

        return user


class QuestionForm(forms.ModelForm):
    tags = forms.CharField(required=False)

    def __init__(self, user, *args, **kwargs):
        super(QuestionForm, self).__init__(*args, **kwargs)
        self.author = user.profile

    def save(self, commit=True):
        instance = super(QuestionForm, self).save(commit=False)
        instance.author = self.author
        instance.save()
        for tag in str(self.data['tags']).split(', '):
            if tag == "":
                continue
            instance.tags.add(Tag.objects.get_or_create(name=tag)[0])
        if commit:
            self.save_m2m()

        return instance

    class Meta:
        model = Question
        fields = ['title', 'text']


class AnswerForm(forms.ModelForm):
    class Meta:
        model = Answer
        fields = ['text']

    def __init__(self, user, question, *args, **kwargs):
        super(AnswerForm, self).__init__(*args, **kwargs)
        self.author = user.profile
        self.question = question

    def save(self, commit=True):
        instance = super(AnswerForm, self).save(commit=False)
        instance.author = self.author
        instance.question = self.question
        instance.question.answer_cnt += 1
        if commit:
            instance.save()
