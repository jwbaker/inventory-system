from django.contrib import messages
from django.contrib.auth.models import User
from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404, render

from uw_users.forms import UserForm


def _collect_messages(request):
    '''
    Loops through stored messages and packages them for consumption.

    We need to iterate through in order to mark the message as seen, otherwise
    it will keep displaying on every page.

    This method also converts the 'error' class into the 'danger' class, so
    bootstrap will recognize and render it properly.

    Positional arguments:
        request - The request object passed to the view
    '''
    storage = messages.get_messages(request)
    message_list = []
    for msg in storage:
        msg_class = msg.tags
        message_list.append({
            'message': msg.message,
            'class': 'danger' if ('error' in msg_class) else msg_class,
        })
    return message_list


def user_detail(request, username):
    if request.user.username == username:
        user = get_object_or_404(User, username=username)

        if request.method == 'POST':
            form = UserForm(request.POST, instance=user)

            if form.is_valid():
                form.save()
                messages.success(request,
                                 'Item saved successfully')
            else:
                messages.error(request,
                               'Something went wrong. Check below for errors')
        else:
            form = UserForm(instance=user)
        message_list = _collect_messages(request)
        return render(request, 'uw_users/user_detail.html', {
            'user': user,
            'form': form,
            'can_edit': True,
            'page_messages': message_list,
            'shown_excluded_fields': [
                {'label': 'Joined', 'value': user.date_joined}
            ],
            'form_id': 'userForm',
        })
    else:
        return HttpResponseForbidden()
