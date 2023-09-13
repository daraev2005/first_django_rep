from .models import *
from django.http import HttpResponseForbidden

class DataMixin:
	model = Task

	def dispatch(self, request, *args, **kwargs):
		task = self.get_object()
		if task.user != self.request.user:
			return HttpResponseForbidden("You do not have permission to this task")
		return super().dispatch(request, *args, **kwargs)