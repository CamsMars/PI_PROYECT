from django.contrib import admin
from .models import *

admin.site.register(usuario)
admin.site.register(CHAT)
admin.site.register(Token)
admin.site.register(MESSAGE)
admin.site.register(PLAYLIST)