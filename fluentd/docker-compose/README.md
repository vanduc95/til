# Usage
Add the following lines to `/etc/rsyslog.conf`:
```
# Send log messages to Fluentd
*.* @127.0.0.1:5140
```
Run docker compose
```
$ docker-compose up
```
