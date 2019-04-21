FROM python:3.4-alpine
ENV http_proxy=http://10.164.177.170:8080
ENV https_proxy=http://10.164.177.170:8080
ADD . /code
WORKDIR /code
RUN pip install -r requirements.txt
CMD ["python", "app.py"]