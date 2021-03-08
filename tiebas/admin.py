from django.contrib import admin

# Register your models here.
from tiebas.models import Topic, poster, Poster_reply
admin.site.register(Topic)
admin.site.register(poster)
admin.site.register(Poster_reply)