from apscheduler.schedulers.background import BackgroundScheduler
from django.utils.deprecation import MiddlewareMixin
from django_apscheduler.jobstores import DjangoJobStore, register_job, register_events


class Scheduler(MiddlewareMixin):

    def process_request(self, request):
        try:
            # 实例化调度器
            scheduler = BackgroundScheduler()
            # 调度器使用DjangoJobStore()
            scheduler.add_jobstore(DjangoJobStore(), "default")

            """
            设置定时任务，选择方式为interval，时间间隔为10s
            另一种方式为每天固定时间执行任务，对应代码为：
            @register_job(scheduler, 'cron', day_of_week='mon-fri', hour='9', minute='30', second='10',id='task_time')
            """

            @register_job(scheduler, "interval", seconds=10)
            def my_job():
                print(11111111111)
                pass

            register_events(scheduler)
            scheduler.start()
        except Exception as e:
            print(e)
            # 有错误就停止定时器
            scheduler.shutdown()
        else:
            return

