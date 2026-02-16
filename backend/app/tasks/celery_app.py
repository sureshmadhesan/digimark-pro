from celery import Celery

from app.core.config import settings

celery = Celery("socialmediapro", broker=settings.redis_url, backend=settings.redis_url)
celery.conf.task_routes = {"app.tasks.reporting.collect_metrics": {"queue": "reporting"}}
celery.conf.broker_connection_retry_on_startup = True
