from django.shortcuts import render

def test(request):
    return render(request, './base.html', {'user': request.user})
