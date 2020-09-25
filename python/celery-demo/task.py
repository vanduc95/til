from celery import Celery
import time

app = Celery('test_celery',
             broker='amqp://ducnv41:ducnv41@localhost/ducnv41_vhost',
             backend='rpc://',
             include=['test_celery.tasks'])

@app.task
def longtime_add(x, y):
    print('long time task begins')
    # sleep 5 seconds
    time.sleep(5)
    print('long time task finished')
    return x + y
