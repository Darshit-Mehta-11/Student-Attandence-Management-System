from django.contrib import admin
from .models import ContactMessage

@admin.register(ContactMessage)
class ContactMessage(admin.ModelAdmin):
    list_display = (['name','email','message'])
    fields = ('name','email','message') 
    list_filter = (['name','email'])
    search_fields = (['name','email'])