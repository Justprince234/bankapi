from django.contrib import admin

from .models import  Contact

# Register your models here.
admin.site.site_header = 'Deunion Reserve'
admin.site.site_title = 'Deunion Reserve'
admin.site.index_title = 'Deunion Reserve Bank Admin'

class ContactAdmin(admin.ModelAdmin):
  list_display = ('id', 'name', 'email', 'phone_number', 'query')
  list_display_links = ('id', 'name')
  search_fields = ('name',)
  list_per_page = 25

admin.site.register(Contact, ContactAdmin)