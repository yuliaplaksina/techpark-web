from django.db import models
from django.conf import settings
from django.db.models import F, Count


class QuestionManager(models.Manager):

    def new(self):
        return self.add_fields().order_by('-data_added')

    def best(self):
        return self.add_fields().order_by('-rating')

    def add_fields(self):
        return self.annotate(
            author_name=F('author__user__username'),
            answer_count=Count('answer'),
            author_avatar=F('author__avatar')
        )


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

    objects = QuestionManager()

    class Meta:
        verbose_name = "Вопрос"
        verbose_name_plural = "Вопросы"

    def __str__(self):
        return self.title


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

    objects = AnswerManager()

    class Meta:
        verbose_name = "Ответ"
        verbose_name_plural = "Ответы"

    def __str__(self):
        return self.text
