from apscheduler.schedulers.background import BackgroundScheduler
from django_apscheduler.jobstores import DjangoJobStore, register_events
from django.utils import timezone
from django_apscheduler.models import DjangoJobExecution
import sys

# This is the function you want to schedule - add as many as you want and then register them in the start() function below
def deactivate_expired_accounts():
    today = timezone.now()
    ...
    print("hello")
    ...


def start():
    scheduler = BackgroundScheduler()
    scheduler.add_jobstore(DjangoJobStore(), "default")
    # run this job every 24 hours
    scheduler.add_job(deactivate_expired_accounts, 'interval', name='clean_accounts', jobstore='default', seconds = 40)
    register_events(scheduler)
    scheduler.start()
    print("Scheduler started...", file=sys.stdout)