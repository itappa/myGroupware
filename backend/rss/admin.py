from django.contrib import admin
from .models import Feed, Entry, Subscription, ReadStatus

admin.site.register(Feed)
admin.site.register(Entry)
admin.site.register(Subscription)
admin.site.register(ReadStatus)