from django.contrib import admin

from .models import Task, Category

class TaskAdmin(admin.ModelAdmin):
	list_display = ('id', 'title', 'completed', 'date_created')
	list_display_links = ('id', 'title')
	search_fields = ('title', 'description')
	list_editable = ('completed',)
	list_filter = ('completed', 'date_created')
	prepopulated_fields = {"slug": ("title",)}

class CategoryAdmin(admin.ModelAdmin):
	search_fields = ('name',)
	list_filter = ('name',)
	prepopulated_fields = {"slug": ("name",)}
	
admin.site.register(Task, TaskAdmin)
admin.site.register(Category, CategoryAdmin)