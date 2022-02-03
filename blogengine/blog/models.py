from django.db import models
from django.shortcuts import reverse
from django.utils.text import slugify
from time import time


def gen_slug(s):
    new_slug = slugify(s, allow_unicode=True)
    return new_slug + '-' + str(int(time()))


class Post(models.Model):
    title = models.CharField(max_length=155, db_index=True, verbose_name='Название поста')
    slug = models.SlugField(max_length=155, blank=True, unique=True)
    body = models.TextField(blank=True, db_index=True, verbose_name='Текст поста')
    tags = models.ManyToManyField('Tag', blank=True, related_name='posts', verbose_name='Название тега')
    date_pub = models.DateTimeField(auto_now_add=True, verbose_name='Дата публикации')

    def get_absolute_url(self):
        return reverse('post_detail_url', kwargs={'slug': self.slug})

    def get_update_url(self):
        return reverse('post_update_url', kwargs={'slug': self.slug})

    def get_delete_url(self):
        return reverse('post_delete_url', kwargs={'slug': self.slug})

    def save(self, *args, **kwargs):
        if not self.id:
            self.slug = gen_slug(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-date_pub']


class Tag(models.Model):
    title = models.CharField(max_length=50, verbose_name='Название тега')
    slug = models.SlugField(max_length=50, unique=True)

    def get_absolute_url(self):
        return reverse('tag_detail_url', kwargs={'slug': self.slug})

    def get_update_url(self):
        return reverse('tag_update_url', kwargs={'slug': self.slug})

    def get_delete_url(self):
        return reverse('tag_delete_url', kwargs={'slug': self.slug})

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-title']
