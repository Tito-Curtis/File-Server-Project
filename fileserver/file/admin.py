from django.contrib import admin
from .models import All_Users, Document, DocumentCategory

# Register your models here.
admin.site.register(All_Users)
admin.site.register(Document)
admin.site.register(DocumentCategory)
