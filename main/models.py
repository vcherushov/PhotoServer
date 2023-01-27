from django.db import models
from django.urls import reverse


class TrackCar(models.Model):
    title = models.CharField(max_length=255, null=True, blank=True)
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name="URL")
    photo = models.ImageField(upload_to="photos/%Y/%m/%d/", verbose_name="Фото")
    time_create = models.DateField(null=True, blank=True, verbose_name="Дата")
    time_time = models.TimeField(null=True, blank=True, verbose_name="Время")
    cat = models.CharField(max_length=255, null=True, blank=True)
    number = models.CharField(max_length=255, null=True, blank=True)


    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('post', kwargs={'post_slug': self.slug})

    class Meta:
        verbose_name = 'Машины'
        verbose_name_plural = 'Машины'
        ordering = ['-time_create']


class Download(models.Model):
    day_start = models.DateField(null=True, blank=True, verbose_name="С")
    day_end = models.DateField(null=True, blank=True, verbose_name="По")
    time_start = models.TimeField(null=True, blank=True, verbose_name="Время")
    time_end = models.TimeField(null=True, blank=True, verbose_name="Время")
    download = models.BooleanField(null=True, blank=True, verbose_name="Скачать")


