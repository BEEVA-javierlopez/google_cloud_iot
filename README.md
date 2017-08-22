# google_cloud_iot
Google Cloud IoT testeting code with Paho and LocustIO

Code to execute stress test:

# locust -i stresslocust.py

And then you have to control test by web browser.

# http://localhost:8089

To create a cluster of instances to increase test with more virtual devices:

# Master instance <- load this first
# locust -i stresslocust.py --master

# Slave instances
# locust -i stresslocust.py --slave --master-host=ip_of_master
