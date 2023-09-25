from datetime import datetime, timedelta
import threading


class Scheduler:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Scheduler, cls).__new__(cls)
            cls._instance.tasks = []
            cls._instance.lock = threading.Lock()
        return cls._instance

    def schedule(self, func, trigger_time, is_recurring=False, interval=None):
        with self.lock:
            task = {
                'func': func,
                'trigger_time': trigger_time,
                'is_recurring': is_recurring,
                'interval': interval
            }
            self.tasks.append(task)

    def run(self):
        while True:

            if not self.tasks:
                break

            now = datetime.now()
            with self.lock:
                for task in self.tasks:
                    if task['trigger_time'] <= now:
                        task['func']()
                        if task['is_recurring']:
                            task['trigger_time'] += task['interval']
                        else:
                            self.tasks.remove(task)


def user_activity_task():
    print("Running user activity task.")
    # Here will be the logic for analyzing user activity


def software_update_task():
    print("Running software update task.")
    # Here is the software update logic


def alarm_task():
    print("Running alarm task.")
    # Here is the logic for triggering the alarm


if __name__ == "__main__":
    scheduler = Scheduler()

    # Schedule a user activity analysis task for every hour
    scheduler.schedule(
        user_activity_task,
        datetime.now() + timedelta(hours=1),
        is_recurring=True,
        interval=timedelta(hours=1)
    )

    # Schedule a software update task every night
    scheduler.schedule(
        software_update_task,
        datetime.now() + timedelta(days=1),
        is_recurring=True,
        interval=timedelta(days=1)
    )

    # Schedule an alarm for every morning at 7:00
    alarm_time = datetime.now().replace(hour=7, minute=0, second=0, microsecond=0)
    if alarm_time < datetime.now():
        alarm_time += timedelta(days=1)
    scheduler.schedule(alarm_task, alarm_time, is_recurring=True, interval=timedelta(days=1))

    scheduler.run()
