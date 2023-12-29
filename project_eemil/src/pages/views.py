from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from .models import TextModel, MessageModel
from django.contrib.auth import login
from .forms import *
from .decorators import admin_required
from django.db import connection
from django.db.models import Q
from django.contrib.auth import update_session_auth_hash
from django.views.decorators.csrf import csrf_protect

#@csrf_protect
@login_required
def deleteTextView(request):
    target_id = request.POST.get('id')
    target = TextModel.objects.get(pk=target_id)
    target.delete()
    return redirect('home')

#@csrf_protect
@login_required
def deleteMessageView(request):
    target_id = request.POST.get('id')
    target = MessageModel.objects.get(pk=target_id)
    target.delete()
    return redirect('home')

#@csrf_protect
@login_required
def deleteTextView2(request):
    target_id = request.POST.get('id')
    target = TextModel.objects.get(pk=target_id)
    target.delete()
    return redirect('submit_text')

#@csrf_protect
@login_required
def deleteMessageView2(request):
    target_id = request.POST.get('id')
    target = MessageModel.objects.get(pk=target_id)
    target.delete()
    return redirect('send_message')

#@csrf_protect
@login_required
def homePageView(request):
    username = request.user.username
    current_user = request.user
    text_items = TextModel.objects.all()
    message_items = MessageModel.objects.filter(message_target=username)
    return render(request, 'pages/index.html', {'text_items': text_items, 'message_items': message_items, 'current_user': current_user})

#@csrf_protect
def register(request):
    if request.method == 'GET':
    #if request.method == 'POST':
        form = SignUpForm(request.GET)
        #form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            return redirect('home')
    else:
        form = SignUpForm()
    return render(request, 'registration/register.html', {'form': form})

@login_required
#@csrf_protect
def submit_text_view(request):
    current_user = request.user
    user_limit, created = TextLimit.objects.get_or_create(user=current_user)
    #if request.method == 'GET':
    if request.method == 'POST':
        #form = TextModelForm(request.GET)
        form = TextModelForm(request.POST)
        username = request.user.username
        if (form.is_valid()):
            if user_limit.can_send_text():
                text_data = form.cleaned_data['text_data']
                TextModel.objects.create(text_data=text_data, username = username)
                user_limit.update_text_count()
                return redirect('submit_text')
    else:
        form = TextModelForm()
    text_items = TextModel.objects.all()
    return render(request, 'pages/submittext.html', {'form': form, 'text_items': text_items, 'current_user': current_user})

@login_required
#@csrf_protect
def send_message_view(request):
    username = request.user.username
    current_user = request.user
    user_limit, created = MessageLimit.objects.get_or_create(user=current_user)
    all_users = User.objects.all()
    #if request.method == 'GET':
    if request.method == 'POST':
        #form = MessageModelForm(request.GET)
        form = MessageModelForm(request.POST)
        if form.is_valid():
            if user_limit.can_send_message():
                message_text = form.cleaned_data['message_text']
                message_sender = username
                message_target_id = form.cleaned_data['message_target']
                message_target = User.objects.get(id=message_target_id)
                MessageModel.objects.create(message_text=message_text, message_sender=message_sender, message_target=message_target)
                user_limit.update_message_count()
                return redirect('send_message')
    else:
        form = MessageModelForm()
    
    message_items = MessageModel.objects.filter(Q(message_target=username) | Q(message_sender=username))
    return render(request, 'pages/sendmessage.html', {'form': form, 'message_items': message_items, 'all_users': all_users})

#@admin_required
@login_required
#@csrf_protect
def show_users_view(request):
    username = request.user.username
    all_users = User.objects.exclude(username=username)
    return render(request, 'pages/users.html', {'all_users': all_users})

#@admin_required
@login_required
#@csrf_protect
def delete_user_view(request):
    username = request.user.username
    all_users = User.objects.exclude(username=username)
    #target_id = request.GET.get('id')
    target_id = request.POST.get('id')
    #print(target_id)
    target = User.objects.get(pk=target_id)
    target.delete()
    return render(request, 'pages/users.html', {'all_users': all_users})

@login_required
#@csrf_protect
def db_injection_view2(request):
    username = request.user.username
    #if request.method == 'GET':
    if request.method == 'POST':
        #form = MessageGetForm(request.GET)
        form = MessageGetForm(request.POST)
        if form.is_valid():
            sender = form.cleaned_data['sender']
            with connection.cursor() as cursor:
                # suitable injection for accessing all messages: ' OR 1=1; --
                query = f"SELECT * FROM pages_messagemodel WHERE message_sender = '{sender}' AND message_target = '{username}'"
                cursor.execute(query)
                # Use of parameterized queries prevents SQL injection
                #query = "SELECT * FROM pages_messagemodel WHERE message_sender = %s AND message_target = %s"
                #cursor.execute(query, [sender, username])
                sql_messages = cursor.fetchall()
                filtered_messages = []
                for message in sql_messages:
                    filtered_messages.append("From " + message[2] + ": " + message[1])
                return render(request, 'pages/getmessages.html',{'form': form, 'filtered_messages': filtered_messages})               
    else:
        form = MessageGetForm()
    return render(request, 'pages/getmessages.html',{'form': form})

@login_required
#@csrf_protect
def personal_info_view(request):
    username = request.user.username
    if request.method == 'GET':
    #if request.method == 'POST':
        form = PersonalInfoForm(request.GET)
        #form = PersonalInfoForm(request.POST)
        print(form.errors)
        if form.is_valid():
            full_name = form.cleaned_data['full_name']
            birthday = form.cleaned_data['birthday']
            phonenumber = form.cleaned_data['phonenumber']
            address = form.cleaned_data['address']
            try:
                model = PersonalInfoModel.objects.get(username=username)
            except PersonalInfoModel.DoesNotExist:
                model = None
            if model:
                model.birthday = birthday
                model.full_name = full_name
                model.phonenumber = phonenumber
                model.address = address
                model.save()
            else:
                PersonalInfoModel.objects.create(username=username, full_name=full_name, birthday=birthday, phonenumber = phonenumber, address=address)
            personal_info = PersonalInfoModel.objects.filter(username=username)
            return render(request, 'pages/personalinfo.html',{'form': form, 'personal_info': personal_info})
    else:
        form = PersonalInfoForm()
    personal_info = PersonalInfoModel.objects.filter(username=username)
    return render(request, 'pages/personalinfo.html', {'form': form, 'personal_info': personal_info})

#@csrf_protect
@login_required
def changepw(request):
    #if request.method == 'GET':
    if request.method == 'POST':
        #form = CustomPasswordChangeForm(request.user, request.GET)
        form = CustomPasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            new_password = form.cleaned_data['new_password1']
            user.set_password(new_password)
            user.save()
            # should update the session for the new password
            update_session_auth_hash(request, user)
            return redirect('home')
    else:
        form = CustomPasswordChangeForm(request.user)
    return render(request, 'registration/changepw.html', {'form': form})
