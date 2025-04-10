import os
import logging
from celery import Celery
from celery.signals import after_setup_logger, after_setup_task_logger

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Initialize Celery
celery = Celery(
    "tasks",
    broker=os.getenv("REDIS_URL", "redis://localhost:6379/0"),
    backend=os.getenv("REDIS_URL", "redis://localhost:6379/0")
)

# Celery configuration
celery.conf.update(
    task_serializer='json',
    accept_content=['json'],
    result_serializer='json',
    timezone='UTC',
    enable_utc=True,
    task_track_started=True,
    task_time_limit=3600,  # 1 hour
    task_soft_time_limit=3300,  # 55 minutes
    worker_max_tasks_per_child=100,
    worker_prefetch_multiplier=1,
    task_acks_late=True,
    task_reject_on_worker_lost=True,
    task_default_queue='default',
    task_queues={
        'default': {
            'exchange': 'default',
            'routing_key': 'default'
        },
        'processing': {
            'exchange': 'processing',
            'routing_key': 'processing'
        }
    }
)

@after_setup_logger.connect
def setup_loggers(logger, *args, **kwargs):
    """Configure logging for Celery"""
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    # Add file handler
    fh = logging.FileHandler('celery.log')
    fh.setFormatter(formatter)
    logger.addHandler(fh)

@after_setup_task_logger.connect
def setup_task_loggers(logger, *args, **kwargs):
    """Configure logging for Celery tasks"""
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    # Add file handler
    fh = logging.FileHandler('celery_tasks.log')
    fh.setFormatter(formatter)
    logger.addHandler(fh)

if __name__ == '__main__':
    celery.start() 