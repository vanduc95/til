#!/usr/bin/env python3
# -*- coding: utf-8 -*-
""" Simple Prometheus exporter for Lets Encrypt metrics from a local certbot. """
import pytz
import re
import time
from datetime import timezone, datetime
from subprocess import check_output
import sys
from prometheus_client import start_http_server, Gauge, Counter, Enum, Summary, Info

CERTBOT_CERTS = Summary(
    "certbot_certs", "Total number of certificates managed by Lets Encrypt"
)

CERTBOT_CERT_EXPIRY_SECONDS = Gauge(
    "certbot_certs_expiry_seconds",
    "Seconds until certificate expiry",
    labelnames=["name", "domains"],
)

CERTBOT_CERT = Enum(
    "certbot_cert",
    "Status of certificate per ACME",
    states=["UNKNOWN", "PENDING", "PROCESSING", "VALID", "INVALID", "REVOKED", "READY"],
    labelnames=["name", "domains"],
)

CERTBOT_CERT_NAMES = Gauge(
    "certbot_cert_names",
    "Number of SANs (subject alternative names) in addition to the common name",
    labelnames=["name"],
)

CERTBOT_CERT_STATUS = Info(
    "certbot_cert_status", "Status of certificate per ACME", labelnames=["name"]
)

CERTBOT_CERT_EXPIRY_COUNTDOWN = Gauge(
    "certbot_cert_expiry_countdown",
    "Countdown—number of seconds until certificate expiry",
    labelnames=["name"],
)


def query_certbot():
    certbot = check_output(["certbot", "certificates"])
    return certbot.decode("utf-8")


def main():
    print(query_certbot())
    certbot_output = query_certbot()

    certificates = []
    cert = {"name": None, "domains": None, "expiry": None}

    certs = re.findall(
        "Certificate Name: .*?Certificate Path:", certbot_output, flags=re.DOTALL
    )

    CERTBOT_CERTS.observe(len(certs))
    for cert in certs:
        name = cert.split("\n")[0].split(": ")[1]
        domains = cert.split("\n")[1].split(": ")[1].split()
        expiry_full = cert.split("Expiry Date: ", 1)[1]
        expiry_status = expiry_full.split(" (")[1].split(":")[0]
        expiry = expiry_full.split(" (")[0]
        # 2019-06-11 14:21:19+00:00
        datetime_object = datetime.strptime(expiry, "%Y-%m-%d %H:%M:%S%z")
        expiry_epoch = int(datetime_object.timestamp())
        now = pytz.UTC.fromutc(datetime.utcnow())
        expiring = expiry_epoch - now.timestamp()
        CERTBOT_CERT_STATUS.labels(name=name).info({"state": expiry_status})
        CERTBOT_CERT.labels(name=name, domains=domains).state(expiry_status)
        CERTBOT_CERT_NAMES.labels(name=name).set(len(domains))
        CERTBOT_CERT_EXPIRY_SECONDS.labels(name=name, domains=domains).set(expiry_epoch)
        CERTBOT_CERT_EXPIRY_COUNTDOWN.labels(name=name).set(expiring)

    start_http_server(8556)
    while True:
        time.sleep(3)


if __name__ == "__main__":
    main()