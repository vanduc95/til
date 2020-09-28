import time

from celery import Celery

app = Celery('test_celery',
             broker='amqp://guest@localhost//',
             backend='rpc://')


@app.task
def longtime_add(x, y):
    print('long time task begins')
    # sleep 5 seconds
    time.sleep(5)
    print('long time task finished')
    return x + y
