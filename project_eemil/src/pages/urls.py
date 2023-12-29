from django.urls import path
from .views import *

urlpatterns = [
    path('', homePageView, name='home'),
    path('delete_text/', deleteTextView, name='delete_text'),
    path('delete_message/', deleteMessageView, name='delete_message'),
    path('delete_text2/', deleteTextView2, name='delete_text2'),
    path('delete_message2/', deleteMessageView2, name='delete_message2'),
    path('register/', register, name='register'),
    path('submit_text/', submit_text_view, name='submit_text'),
    path('send_message/', send_message_view, name='send_message'),
    #path('axes/', include('axes.urls', namespace='axes')),
    path('users/', show_users_view, name='show_users'),
    path('delete_user/', delete_user_view, name='delete_user'),
    path('getmessages/', db_injection_view2, name='get_messages'),
    path('personalinfo/', personal_info_view, name='personal_info'),
    path('pw_change/', changepw, name='pw_change'),
]
