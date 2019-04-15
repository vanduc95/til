# Usage
Add the following lines to `/etc/rsyslog.conf`:
```
# Send log messages to Fluentd
*.* @127.0.0.1:5140
```
Restart rsyslog service
```
$ sudo systemctl restart rsyslog.service
```
Run docker compose
```
$ cd syslog
$ docker-compose up -d
```

# Test
Run command with user `root` or `ssh`. Example
```
$ ssh <user>@<ip>
## or
$ sudo su
```
Verify with `docker logs`
```
$ docker logs --tail 50 -f fluentd

```