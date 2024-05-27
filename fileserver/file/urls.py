from django.urls import path
from . import views

urlpatterns = [
    path('',views.index,name='index'),
    path('signup/',views.signup_view,name='signup'),
    path('login/',views.login_view,name='login'),
    path('logout/',views.logout_view,name='logout'),
    path('feed/',views.feed_page_view,name='feed_page'),
    path('download/<int:document_id>',views.download_document_view,name='download_document'),
    path('send/<int:document_id>',views.send_email_view,name='send_email'),
    path('view/<int:document_id>',views.view_documents,name='view_documents'),
    path('filter/',views.filter_category_view,name='filter_document'),
    path('search/',views.search_document_view,name='search'),
    path('contact_admin/',views.contact_admin_view,name='contact_admin'),
]