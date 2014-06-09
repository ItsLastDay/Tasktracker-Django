from django.shortcuts import render, redirect
from django.views.decorators.http import require_GET, require_POST
from tasktracker.models import * 
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.forms import UserCreationForm
from time import strftime

@require_GET
def home(request):
    sort_choices = ['Latest', 'Popular', 'Urgent']
    numpage_choices = ['5', '10', '20', '50']
    
    default_sort = sort_choices[0]
    default_numpage = numpage_choices[0]
    default_page = 1

    all_tasks = Task.objects.valid()

    request.session.setdefault('sort', default_sort)
    request.session.setdefault('tasks_on_page', default_numpage)
    request.session.setdefault('page', default_page)
    request.session.setdefault('show_closed', False)

    sort_order = request.GET.get('sort', request.session['sort'])
    request.session['sort'] = sort_order
    
    if not request.session['show_closed'] == 'on':
        all_tasks = Task.objects.valid().filter(status=Task.OPEN)

    if sort_order == 'Urgent':
        all_tasks = all_tasks.order_by('-expiration_date', '-created_on')
    elif sort_order == 'Popular':
        all_tasks = all_tasks.order_by('-rating', '-created_on')


    tasks_on_page = request.session.get('tasks_on_page')
    
    all_tasks.defer('description', 'id')
    
    paginator = Paginator(all_tasks, tasks_on_page)

    page = request.GET.get('page', request.session.get('page'))
    try:
        tasks = paginator.page(page)
    except PageNotAnInteger:
        tasks = paginator.page(1)
    except EmptyPage:
        tasks = paginator.page(paginator.num_pages)


    data = dict()
    data['tasks'] = tasks
    data['sort_order'] = sort_order
    data['sort_choices'] = sort_choices
    data['show_closed'] = request.session['show_closed']
    data['numpage_choices'] = numpage_choices
    data['tasks_on_page'] = tasks_on_page
    data['page'] = page
    return render(request, 'home.html', data)

@require_POST
def home_submit(request):
    for form_value in ['page', 'tasks_on_page', 'show_closed']:
        if form_value in request.POST:
            request.session[form_value] = request.POST[form_value]
        else:
            request.session[form_value] = 0
    return redirect('/home/', permanent=True) 

def userlist(request):
    return render(request, 'userlist.html', {'userlist': User.objects.all()})

def user(request, login):
    data = dict()
    try:
        x = User.objects.get(username__exact=login)
        data['person'] = x
    except:
        data['error_message'] = 'No such user!'

    return render(request, 'user.html', data)
    

def profile(request):
    if not request.user.is_authenticated():
        return redirect('/home/', permanent=True)
    return render(request, 'profile.html', {})

def task(request, tid):
    try:
        task = Task.objects.get(id=tid)
    except:
        return render(request, 'task.html', {"error_message": "Task was not found!"})

    data = dict()
    data['task'] = task
    return render(request, 'task.html', data)

def logout_view(request):
    logout(request)
    return redirect('/home/', permanent=True)

def registration_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            username = form.clean_username()
            pswd = form.clean_password2()
            new_client = User(username=username, password=pswd, \
                    registration_date=strftime('%Y-%m-%d %H:%M'))
            new_client.set_password(pswd)
            new_client.save()
            return redirect('/userlist/', permanent=True)
    else:
        form = UserCreationForm()

    return render(request, 'register.html', {'form': form})
    

@require_GET
def login_view(request):
    msg = ''
    if 'login_error_message' in request.session:
        msg = request.session['login_error_message']
        del request.session['login_error_message']
    return render(request, 'login.html', {'error_message': msg})

@require_POST
def login_view_post(request):
    name = request.POST['username']
    password = request.POST['password']
    user = authenticate(username=name, password=password)
    if user is not None:
        login(request, user)
        return redirect('/home/', permanent=True)
    else:
        request.session['login_error_message'] = 'Username/password did not match \
                anything'
        return redirect('/login/', permanent=True)
