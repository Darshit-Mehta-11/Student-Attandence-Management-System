from .models import Result, Fee
from django.contrib import admin


@admin.register(Result)
class Result(admin.ModelAdmin):
    list_display = ('student','sem')
    fields = ('student','sem','seo','c_sharp','php','python','java','ac_year') 
    list_filter = (['student','sem'])
    search_fields = (['student','sem'])


@admin.register(Fee)
class FeeAdmin(admin.ModelAdmin):
    list_display = ('student','semester','amount','paid','paid_on')
    list_filter = ('semester','paid')
    search_fields = ('student__username','student__email')