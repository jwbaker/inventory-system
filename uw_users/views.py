from django.contrib.auth.models import User
from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404, render


def user_detail(request, username):
    if request.user.username == username:
        user = get_object_or_404(User, username=username)
        return render(request, 'uw_users/user_detail.html', {
            'user': user
        })
    else:
        return HttpResponseForbidden()
