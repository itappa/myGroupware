from django.shortcuts import render
from .models import Item

def list_items(request):
    context = {
        "items": Item.objects.all(),
    }
    return render(request, "bookmark/list_items.html", context)