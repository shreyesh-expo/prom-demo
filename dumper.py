import sys
import os

from prometheus_client import start_http_server, Gauge, Counter
from postgres import *
from typing import List,Dict

PROMETHEUS_PORT = int(os.getenv('PROMETHEUS_PORT', 7000))

project_ids:List[str] = ['project_a', 'project_b']
venue_ids:List[PGVenue] = ['venue_a', 'venue_b']

LabelValues:Dict[str,List] = {
    # 'camera': [f'camera_{n}' for n in range(1,10)],
    'project': project_ids,
    'venue': venue_ids,
    # 'zone': [f'zone_{n}' for n in list("1234")],
    # 'block': [f'block_{n}' for n in list("abcdef")],
    # 'cluster': [f'cluster_{n}' for n in list("lmnop")],
}

#- Start up the server to expose the metrics
start_http_server(PROMETHEUS_PORT)
PrometheusHelperDict:Dict[str,Any] = {}

#- Metric with labels
line_crossing_count_in = Counter(name='line_crossing_count_in', documentation='', labelnames=list(LabelValues.keys()))
line_crossing_count_out = Counter(name='line_crossing_count_out', documentation='', labelnames=list(LabelValues.keys()))
total_count = Gauge(name='count', documentation='', labelnames=list(LabelValues.keys()))

import signal

def alarm_handler(signum, frame):
    print("Exiting due to SIGALRM")
    sys.exit(0)
# Set the signal handler for SIGALRM

if __name__ == '__main__':
    signal.signal(signal.SIGALRM, alarm_handler)
    signal.alarm(3600)
    while True:
        try:
            metric_label_dict = {}
            for label_name in LabelValues.keys():
                metric_label_dict.update({label_name: random.choice(LabelValues[label_name])})
            line_crossing_count_in.labels(**metric_label_dict).inc(int(random.uniform(7,10)))
            line_crossing_count_out.labels(**metric_label_dict).inc(int(random.uniform(1,10)))
            total_count.labels(**metric_label_dict).set(random.uniform(1,10))
            print(f'Dumping Prometheus Data: {metric_label_dict}')
        except: pass
        timesleep.sleep(30)