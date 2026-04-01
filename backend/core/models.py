from django.db import models

class Workflow(models.Model):
    name = models.CharField(max_length=255)
    category = models.CharField(max_length=255, blank=True, default="")
    trigger = models.CharField(max_length=50, choices=[("manual", "Manual"), ("scheduled", "Scheduled"), ("event", "Event"), ("webhook", "Webhook")], default="manual")
    status = models.CharField(max_length=50, choices=[("active", "Active"), ("inactive", "Inactive"), ("draft", "Draft")], default="active")
    steps_count = models.IntegerField(default=0)
    runs = models.IntegerField(default=0)
    last_run = models.DateField(null=True, blank=True)
    description = models.TextField(blank=True, default="")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.name

class WorkflowStep(models.Model):
    workflow_name = models.CharField(max_length=255)
    step_name = models.CharField(max_length=255, blank=True, default="")
    step_type = models.CharField(max_length=50, choices=[("action", "Action"), ("condition", "Condition"), ("delay", "Delay"), ("notification", "Notification")], default="action")
    position = models.IntegerField(default=0)
    config = models.TextField(blank=True, default="")
    active = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.workflow_name

class Execution(models.Model):
    workflow_name = models.CharField(max_length=255)
    started_at = models.DateField(null=True, blank=True)
    completed_at = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=50, choices=[("running", "Running"), ("completed", "Completed"), ("failed", "Failed"), ("cancelled", "Cancelled")], default="running")
    steps_completed = models.IntegerField(default=0)
    error_message = models.TextField(blank=True, default="")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.workflow_name
