from django.shortcuts import render


def permission_denied(request):
    return render(request, 'errors/403.html')
