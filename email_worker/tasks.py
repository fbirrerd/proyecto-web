from celery import Celery

app = Celery('tasks', broker='redis://redis_db:6379/0')

@app.task
def send_email(to, subject, body):
    print(f"Sending email to {to} with subject {subject}")
