import json
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.db.models import Sum, Count
from .models import Workflow, WorkflowStep, Execution


def login_view(request):
    if request.user.is_authenticated:
        return redirect('/dashboard/')
    error = ''
    if request.method == 'POST':
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('/dashboard/')
        error = 'Invalid credentials. Try admin / Admin@2024'
    return render(request, 'login.html', {'error': error})


def logout_view(request):
    logout(request)
    return redirect('/login/')


@login_required
def dashboard_view(request):
    ctx = {}
    ctx['workflow_count'] = Workflow.objects.count()
    ctx['workflow_manual'] = Workflow.objects.filter(trigger='manual').count()
    ctx['workflow_scheduled'] = Workflow.objects.filter(trigger='scheduled').count()
    ctx['workflow_event'] = Workflow.objects.filter(trigger='event').count()
    ctx['workflowstep_count'] = WorkflowStep.objects.count()
    ctx['workflowstep_action'] = WorkflowStep.objects.filter(step_type='action').count()
    ctx['workflowstep_condition'] = WorkflowStep.objects.filter(step_type='condition').count()
    ctx['workflowstep_delay'] = WorkflowStep.objects.filter(step_type='delay').count()
    ctx['execution_count'] = Execution.objects.count()
    ctx['execution_running'] = Execution.objects.filter(status='running').count()
    ctx['execution_completed'] = Execution.objects.filter(status='completed').count()
    ctx['execution_failed'] = Execution.objects.filter(status='failed').count()
    ctx['recent'] = Workflow.objects.all()[:10]
    return render(request, 'dashboard.html', ctx)


@login_required
def workflow_list(request):
    qs = Workflow.objects.all()
    search = request.GET.get('search', '')
    if search:
        qs = qs.filter(name__icontains=search)
    status_filter = request.GET.get('status', '')
    if status_filter:
        qs = qs.filter(trigger=status_filter)
    return render(request, 'workflow_list.html', {'records': qs, 'search': search, 'status_filter': status_filter})


@login_required
def workflow_create(request):
    if request.method == 'POST':
        obj = Workflow()
        obj.name = request.POST.get('name', '')
        obj.category = request.POST.get('category', '')
        obj.trigger = request.POST.get('trigger', '')
        obj.status = request.POST.get('status', '')
        obj.steps_count = request.POST.get('steps_count') or 0
        obj.runs = request.POST.get('runs') or 0
        obj.last_run = request.POST.get('last_run') or None
        obj.description = request.POST.get('description', '')
        obj.save()
        return redirect('/workflows/')
    return render(request, 'workflow_form.html', {'editing': False})


@login_required
def workflow_edit(request, pk):
    obj = get_object_or_404(Workflow, pk=pk)
    if request.method == 'POST':
        obj.name = request.POST.get('name', '')
        obj.category = request.POST.get('category', '')
        obj.trigger = request.POST.get('trigger', '')
        obj.status = request.POST.get('status', '')
        obj.steps_count = request.POST.get('steps_count') or 0
        obj.runs = request.POST.get('runs') or 0
        obj.last_run = request.POST.get('last_run') or None
        obj.description = request.POST.get('description', '')
        obj.save()
        return redirect('/workflows/')
    return render(request, 'workflow_form.html', {'record': obj, 'editing': True})


@login_required
def workflow_delete(request, pk):
    obj = get_object_or_404(Workflow, pk=pk)
    if request.method == 'POST':
        obj.delete()
    return redirect('/workflows/')


@login_required
def workflowstep_list(request):
    qs = WorkflowStep.objects.all()
    search = request.GET.get('search', '')
    if search:
        qs = qs.filter(workflow_name__icontains=search)
    status_filter = request.GET.get('status', '')
    if status_filter:
        qs = qs.filter(step_type=status_filter)
    return render(request, 'workflowstep_list.html', {'records': qs, 'search': search, 'status_filter': status_filter})


@login_required
def workflowstep_create(request):
    if request.method == 'POST':
        obj = WorkflowStep()
        obj.workflow_name = request.POST.get('workflow_name', '')
        obj.step_name = request.POST.get('step_name', '')
        obj.step_type = request.POST.get('step_type', '')
        obj.position = request.POST.get('position') or 0
        obj.config = request.POST.get('config', '')
        obj.active = request.POST.get('active') == 'on'
        obj.save()
        return redirect('/workflowsteps/')
    return render(request, 'workflowstep_form.html', {'editing': False})


@login_required
def workflowstep_edit(request, pk):
    obj = get_object_or_404(WorkflowStep, pk=pk)
    if request.method == 'POST':
        obj.workflow_name = request.POST.get('workflow_name', '')
        obj.step_name = request.POST.get('step_name', '')
        obj.step_type = request.POST.get('step_type', '')
        obj.position = request.POST.get('position') or 0
        obj.config = request.POST.get('config', '')
        obj.active = request.POST.get('active') == 'on'
        obj.save()
        return redirect('/workflowsteps/')
    return render(request, 'workflowstep_form.html', {'record': obj, 'editing': True})


@login_required
def workflowstep_delete(request, pk):
    obj = get_object_or_404(WorkflowStep, pk=pk)
    if request.method == 'POST':
        obj.delete()
    return redirect('/workflowsteps/')


@login_required
def execution_list(request):
    qs = Execution.objects.all()
    search = request.GET.get('search', '')
    if search:
        qs = qs.filter(workflow_name__icontains=search)
    status_filter = request.GET.get('status', '')
    if status_filter:
        qs = qs.filter(status=status_filter)
    return render(request, 'execution_list.html', {'records': qs, 'search': search, 'status_filter': status_filter})


@login_required
def execution_create(request):
    if request.method == 'POST':
        obj = Execution()
        obj.workflow_name = request.POST.get('workflow_name', '')
        obj.started_at = request.POST.get('started_at') or None
        obj.completed_at = request.POST.get('completed_at') or None
        obj.status = request.POST.get('status', '')
        obj.steps_completed = request.POST.get('steps_completed') or 0
        obj.error_message = request.POST.get('error_message', '')
        obj.save()
        return redirect('/executions/')
    return render(request, 'execution_form.html', {'editing': False})


@login_required
def execution_edit(request, pk):
    obj = get_object_or_404(Execution, pk=pk)
    if request.method == 'POST':
        obj.workflow_name = request.POST.get('workflow_name', '')
        obj.started_at = request.POST.get('started_at') or None
        obj.completed_at = request.POST.get('completed_at') or None
        obj.status = request.POST.get('status', '')
        obj.steps_completed = request.POST.get('steps_completed') or 0
        obj.error_message = request.POST.get('error_message', '')
        obj.save()
        return redirect('/executions/')
    return render(request, 'execution_form.html', {'record': obj, 'editing': True})


@login_required
def execution_delete(request, pk):
    obj = get_object_or_404(Execution, pk=pk)
    if request.method == 'POST':
        obj.delete()
    return redirect('/executions/')


@login_required
def settings_view(request):
    return render(request, 'settings.html')


@login_required
def api_stats(request):
    data = {}
    data['workflow_count'] = Workflow.objects.count()
    data['workflowstep_count'] = WorkflowStep.objects.count()
    data['execution_count'] = Execution.objects.count()
    return JsonResponse(data)
