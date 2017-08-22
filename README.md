# Benchmark Google Cloud IoT
Google Cloud IoT testeting code with Paho and LocustIO

# Single benchmark

Code to execute stress test:

locust -i stresslocust.py

And then you have to control test using web browser.

http://localhost:8089


# Cluster benchmark

To create a cluster of instances to increase test with more virtual devices:

**Master instance (load this first)**

locust -i stresslocust.py --master

**Slave instances**

locust -i stresslocust.py --slave --master-host=ip_of_master

And then you have to control test using web browser.

http://ip_of_master:8089
