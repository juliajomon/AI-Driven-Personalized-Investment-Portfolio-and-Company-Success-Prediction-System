from apscheduler.schedulers.background import BackgroundScheduler
from services.scheduler_service import check_saved_portfolios

scheduler = BackgroundScheduler()

scheduler.add_job(
    check_saved_portfolios,
    trigger="cron",
    day_of_week="mon",
    hour=8
)