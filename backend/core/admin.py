from django.contrib import admin
from .models import Workflow, WorkflowStep, Execution

@admin.register(Workflow)
class WorkflowAdmin(admin.ModelAdmin):
    list_display = ["name", "category", "trigger", "status", "steps_count", "created_at"]
    list_filter = ["trigger", "status"]
    search_fields = ["name", "category"]

@admin.register(WorkflowStep)
class WorkflowStepAdmin(admin.ModelAdmin):
    list_display = ["workflow_name", "step_name", "step_type", "position", "active", "created_at"]
    list_filter = ["step_type"]
    search_fields = ["workflow_name", "step_name"]

@admin.register(Execution)
class ExecutionAdmin(admin.ModelAdmin):
    list_display = ["workflow_name", "started_at", "completed_at", "status", "steps_completed", "created_at"]
    list_filter = ["status"]
    search_fields = ["workflow_name"]
