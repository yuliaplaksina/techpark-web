from django.db import models
from django.conf import settings
from django.db.models import F, Count


class QuestionManager(models.Manager):

    def new(self):
        return self.add_author().order_by('-data_added')

    def best(self):
        return self.add_author().order_by('-rating')

    def tag(self, tag):
        return self.add_author().filter(tags=tag)

    def add_author(self):
        return self.annotate(
            author_name=F('author__user__username'),
            author_avatar=F('author__avatar')
        )

    def add_answer_count(self):
        return self.annotate(answer_count=Count('answer'))


class Question(models.Model):
    title = models.CharField(
        max_length=255,
        verbose_name="Название"
    )
    text = models.TextField(verbose_name="Текст")
    data_added = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Дата публикации"
    )
    rating = models.IntegerField(default=0)
    author = models.ForeignKey(
        'Profile',
        on_delete=models.CASCADE
    )
    tags = models.ManyToManyField(
        'Tag'
    )
    answer_cnt = models.IntegerField(default=0)
    likes = models.ManyToManyField(
        to='Profile',
        through='QuestionLike',
        related_name='liked_questions'
    )

    objects = QuestionManager()

    class Meta:
        verbose_name = "Вопрос"
        verbose_name_plural = "Вопросы"

    def __str__(self):
        return self.title


class QuestionLike(models.Model):
    question = models.ForeignKey(
        to=Question,
        on_delete=models.CASCADE
    )
    profile = models.ForeignKey(
        to='Profile',
        on_delete=models.CASCADE
    )


class Tag(models.Model):
    name = models.CharField(
        max_length=255,
        verbose_name="Тег",
        unique=True
    )

    class Meta:
        verbose_name = "Тег"
        verbose_name_plural = "Теги"

    def __str__(self):
        return self.name


# class QuestionTag(models.Model):
#     question = models.ForeignKey(Question, on_delete=models.CASCADE)
#     tag = models.ForeignKey(Tag, on_delete=models.CASCADE)


class Profile(models.Model):

    user = models.OneToOneField(
        to=settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    rating = models.IntegerField(verbose_name="Рейтинг", default=0)
    avatar = models.ImageField(
        verbose_name="Аватарка",
        upload_to='img/%Y/%m/%d',
        default='img/test.jpg'
    )

    class Meta:
        verbose_name = "Профиль"
        verbose_name_plural = "Профили"

    def __str__(self):
        return self.user.username


class AnswerManager(models.Manager):

    def add_fields(self):
        return self.annotate(
            author_name=F('author__user__username'),
            author_avatar=F('author__avatar')
        )


class Answer(models.Model):
    text = models.TextField(verbose_name="Текст")
    author = models.ForeignKey(
        'Profile',
        on_delete=models.CASCADE
    )
    question = models.ForeignKey(
        'Question',
        on_delete=models.CASCADE
    )
    data_added = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Дата публикации"
    )
    is_right = models.BooleanField(default=False)
    rating = models.IntegerField(verbose_name="Рейтинг", default=0)
    likes = models.ManyToManyField(
        to=Profile,
        through='AnswerLike',
        related_name='liked_answers'
    )
    objects = AnswerManager()

    # def save(self, *args, **kwargs):
    #     super(Answer, self).save(*args, **kwargs)
    #     self.question.answer_cnt += 1
    #     self.question.save()

    class Meta:
        verbose_name = "Ответ"
        verbose_name_plural = "Ответы"

    def __str__(self):
        return self.text


class AnswerLike(models.Model):
    answer = models.ForeignKey(
        to=Answer,
        on_delete=models.CASCADE
    )
    profile = models.ForeignKey(
        to=Profile,
        on_delete=models.CASCADE
    )
