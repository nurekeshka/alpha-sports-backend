from apps.core.models import User
from django.db import models


class Photo(models.Model):
    link = models.URLField(null=True, blank=True, unique=True, verbose_name='link')

    class Meta:
        verbose_name = 'photo'
        verbose_name_plural = 'photos'
        ordering = ('link',)

    def __str__(self):
        return self.link


class Feedback(models.Model):
    raiting = models.FloatField(verbose_name='raiting')
    description = models.TextField(null=True, blank=True, verbose_name='description')
    user = models.ForeignKey(User, on_delete=models.PROTECT, verbose_name='user')
    field = models.ForeignKey('Field', on_delete=models.PROTECT, verbose_name='field')

    class Meta:
        verbose_name = 'feedback'
        verbose_name_plural = 'feedbacks'
        ordering = ('field', 'user')

    def __str__(self):
        return str(self.raiting)


class Field(models.Model):
    address = models.CharField(max_length=254, verbose_name='address')
    latitude = models.FloatField(null=True, blank=True, verbose_name='latitude')
    longitude = models.FloatField(null=True, blank=True, verbose_name='longitude')
    photo = models.ForeignKey(Photo, on_delete=models.CASCADE, verbose_name='photo')
    contacts = models.TextField(blank=True, verbose_name='contacts')

    class Meta:
        verbose_name = 'field'
        verbose_name_plural = 'fields'
        ordering = ('address',)
    
    def __str__(self):
        return self.address
    
    def calculate_rate(self):
        feedbacks = Feedback.objects.filter(field=self)
        
        summary = 0
        count = len(feedbacks)

        for i in range(count):
            summary += feedbacks[i].raiting

        return summary / count


class Team(models.Model):
    name = models.CharField(max_length=50, verbose_name='name')
    players = models.ManyToManyField(User, blank=True, verbose_name='players')
    game = models.ForeignKey('Game', blank=True, on_delete=models.CASCADE, verbose_name='game')

    class Meta:
        verbose_name = 'team'
        verbose_name_plural = 'teams'
        ordering = ('game',)
    
    def __str__(self):
        return self.name


class Game(models.Model):
    field = models.ForeignKey(Field, on_delete=models.PROTECT, verbose_name='field')
    form = models.IntegerField(verbose_name='form')
    date = models.DateField(auto_now=False, auto_now_add=False, verbose_name='date')
    start = models.TimeField(auto_now=False, auto_now_add=False, verbose_name='start')
    end = models.TimeField(auto_now=False, auto_now_add=False, verbose_name='end')
    teams = models.ManyToManyField(Team, blank=True, verbose_name='teams')

    class Meta:
        verbose_name = 'game'
        verbose_name_plural = 'games'
        ordering = ('date', 'field')
    
    def __str__(self):
        return self.field.address + ' || ' + str(self.form)
