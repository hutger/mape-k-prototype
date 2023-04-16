#!/usr/bin/env python3

import mape
import requests
import time
import sys
from datetime import datetime

sensored_endpoint = "http://www.randomnumberapi.com/api/v1.0/random?min=0&max=1000&count=1"

mape.init()

# Risk loop definition, named "risk"
loop = mape.Loop(uid='risk') #

# MONITOR
# Monitor element of risk loop
@loop.monitor #
def detect(risk, on_next): #
    on_next(risk)

# ----

# PLAN
@loop.plan(uid='custom_policy') #
def policy(risk, on_next, self):
    # Risk plans
    if risk in self.critical_risk_range:
        on_next({'risk_level': 'Critical'}) #
        on_next({'public_access': False})
    elif risk in self.high_risk_range:
        on_next({'risk_level': 'High'}) #
        on_next({'public_access': False})
    elif risk in self.medium_risk_range:
        on_next({'risk_level': 'Medium'}) #
        on_next({'public_access': True})
    else:
        on_next({'risk_level': 'Low'}) #
        on_next({'public_access': True})

policy.critical_risk_range = range(750, 1000)
policy.high_risk_range = range(500, 749)
policy.medium_risk_range = range(250, 499)


# ----
# EXECUTE
@loop.execute
def exec(item, on_next):
    if 'risk_level' in item:
        print(f"Risk Level: {item['risk_level']}")
    if 'public_access' in item:
        print(f"Public Access: {'Allowed' if item['public_access'] else 'Blocked'}")

# ----
# SUBSCRIBE

detect.subscribe(policy)
policy.subscribe(exec)

# stdout
def print_to_stdout(*a):

    print(*a, file=sys.stdout)

# ----

# SENSOR
def sensor():
    while True:
        response = requests.get(sensored_endpoint)
        sensored_input = (response.json())[0]

        # Trigger
        print_to_stdout("----")
        print_to_stdout(datetime.now())
        detect.start()
        detect(sensored_input)
        print_to_stdout("----\n")

        time.sleep(1)

if __name__ == "__main__":
    sensor()