from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from core.models import Workflow, WorkflowStep, Execution
from datetime import date, timedelta
import random


class Command(BaseCommand):
    help = 'Seed NexusFlow with demo data'

    def handle(self, *args, **kwargs):
        if not User.objects.filter(username='admin').exists():
            User.objects.create_superuser('admin', 'admin@nexusflow.com', 'Admin@2024')
            self.stdout.write(self.style.SUCCESS('Admin user created'))

        if Workflow.objects.count() == 0:
            for i in range(10):
                Workflow.objects.create(
                    name=f"Sample Workflow {i+1}",
                    category=f"Sample {i+1}",
                    trigger=random.choice(["manual", "scheduled", "event", "webhook"]),
                    status=random.choice(["active", "inactive", "draft"]),
                    steps_count=random.randint(1, 100),
                    runs=random.randint(1, 100),
                    last_run=date.today() - timedelta(days=random.randint(0, 90)),
                    description=f"Sample description for record {i+1}",
                )
            self.stdout.write(self.style.SUCCESS('10 Workflow records created'))

        if WorkflowStep.objects.count() == 0:
            for i in range(10):
                WorkflowStep.objects.create(
                    workflow_name=f"Sample WorkflowStep {i+1}",
                    step_name=f"Sample WorkflowStep {i+1}",
                    step_type=random.choice(["action", "condition", "delay", "notification"]),
                    position=random.randint(1, 100),
                    config=f"Sample config for record {i+1}",
                    active=random.choice([True, False]),
                )
            self.stdout.write(self.style.SUCCESS('10 WorkflowStep records created'))

        if Execution.objects.count() == 0:
            for i in range(10):
                Execution.objects.create(
                    workflow_name=f"Sample Execution {i+1}",
                    started_at=date.today() - timedelta(days=random.randint(0, 90)),
                    completed_at=date.today() - timedelta(days=random.randint(0, 90)),
                    status=random.choice(["running", "completed", "failed", "cancelled"]),
                    steps_completed=random.randint(1, 100),
                    error_message=f"Sample error message for record {i+1}",
                )
            self.stdout.write(self.style.SUCCESS('10 Execution records created'))
