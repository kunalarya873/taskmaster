from django.shortcuts import render, redirect
from .models import Task
from .forms import TaskForm

def task_list(request):
    status_filter = request.GET.get('status', None)
    sort_by = request.GET.get('sort_by', 'due_date')

    tasks = Task.objects.all()

    if status_filter:
        tasks = tasks.filter(status=status_filter)

    tasks = tasks.order_by(sort_by)

    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('task_list')
    else:
        form = TaskForm()

    return render(request, 'tasks/task_list.html', {'tasks': tasks, 'form': form})
