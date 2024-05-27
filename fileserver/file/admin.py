from django.contrib import admin
from .models import All_Users, Document, DocumentCategory,ContactAdmin

# Register your models here.



class UserDashboard(admin.ModelAdmin):
    list_display = ('id','firstName', 'lastName', 'email','last_login')
    list_display_links = ('id','firstName', 'lastName')
    fields = ('id','firstName', 'lastName', 'email','date_created','last_login',
              'is_active','is_staff','is_admin')
    readonly_fields =['id','firstName', 'lastName', 'email','password','is_active','date_created','last_login']
    search_fields = ['firstName','lastName']
    list_filter = ['is_admin','is_active']
    def has_add_permission(self, request) :
        
        return not request.user.is_staff
    
class DocumentDashboard(admin.ModelAdmin):
    list_display = ('title','category','email_sent','download_times','users_length')

    readonly_fields = ['email_count','download_count']
    filter_horizontal = ['assigned_user']
    search_fields = ('title',)
    list_filter = ('category',)
    
    def email_sent(self,rec):
        return rec.email_count
    email_sent.short_description = 'Email Sent'
    
    def download_times(self,rec):
        return rec.download_count
    download_times.short_description = 'Number of downloads'
    
    def users_length(self,rec):
        user = rec.assigned_user.all().count()
        return user
    users_length.short_description = 'Users assigned to'

class ContactAdminDashboard(admin.ModelAdmin):
    readonly_fields = ('title','message','user','user_id')
    list_display = ('id','title','user','user_id','created_at')
    list_display_links = ('id','title')
    def has_add_permission(self, request) :
        
        return not request.user.is_staff
    def has_change_permission(self, request,obj=None):
        return not request.user.is_staff
    def user_id(self,rec):
        return rec.user.id
    user_id.short_description = 'User ID'
class DocumentCategoryDashboard(admin.ModelAdmin):
    list_display = ('id', 'category_name' )
    list_display_links = ('id', 'category_name')



admin.site.register(All_Users,UserDashboard)
admin.site.register(Document,DocumentDashboard)
admin.site.register(DocumentCategory,DocumentCategoryDashboard)
admin.site.register(ContactAdmin,ContactAdminDashboard)

admin.site.site_header = "File Server Administration"
admin.site.site_title = "Fileserver admin"
admin.site.index_title ="Files"