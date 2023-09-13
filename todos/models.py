from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User

 
class Task(models.Model):
	title = models.CharField(max_length=200, verbose_name='Заголовок')
	slug = models.SlugField(max_length=30, null=False, unique=True, db_index=True, verbose_name="URL")
	description = models.TextField(verbose_name='Описание')
	completed = models.BooleanField(default=False, verbose_name='Выполнено')
	date_created = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
	cat = models.ForeignKey('Category', on_delete=models.CASCADE, null='True', verbose_name='Категория')
	user = models.ForeignKey(User, on_delete=models.CASCADE)

	class Meta:
		verbose_name = ("Задачу") 
		verbose_name_plural = ("Задачи")
		ordering = ['date_created'] 
		
	def __str__(self):
		return self.title 

	def get_absolute_url(self):
		return reverse('detail', kwargs={'detail_slug': self.slug})

class Category(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	slug = models.SlugField(max_length=255, null=False, unique=True, db_index=True, verbose_name="URL")
	name = models.CharField(max_length=100, db_index=True, verbose_name='Наименование')

	def __str__(self):
		return self.name

	class Meta:
		verbose_name = ("Категорию") 
		verbose_name_plural = ("Категории")

	def get_absolute_url(self):
		return reverse('cat', kwargs={'cat_slug': self.slug})