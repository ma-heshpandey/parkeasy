from apscheduler.schedulers.background import BackgroundScheduler
from .import background_program

def start():
    schedular=BackgroundScheduler()
    schedular.add_job(background_program.car_time_check,'interval',seconds=5)
    schedular.start()