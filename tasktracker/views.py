from django.shortcuts import render, redirect
from django.views.decorators.http import require_GET, require_POST
from tasktracker.models import * 
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

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

    if request.session.get('sort') == 'Urgent':
        all_tasks = all_tasks.order_by('-expiration_date', '-created_on')
    elif request.session.get('sort') == 'Popular':
        all_tasks = all_tasks.order_by('-rating', '-created_on')

    if not request.session['show_closed']:
        all_tasks = Task.objects.valid().filter(status=Task.OPEN)

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
    data['sort_order'] = request.session.get('sort')
    data['user'] = request.user
    data['sort_choices'] = sort_choices
    data['numpage_choices'] = numpage_choices
    data['tasks_on_page'] = tasks_on_page
    data['page'] = page
    data['ps'] = request.session
    return render(request, 'home.html', data)

@require_POST
def home_submit(request):
    for form_value in ['page', 'tasks_on_page']:
        if form_value in request.POST:
            request.session[form_value] = request.POST[form_value]
    return redirect('/home/', permanent=True) 

def userlist(request):
    return render(request, 'userlist.html')

def user(request, login):
    pass

def task(request, tid):
    pass
