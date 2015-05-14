Pigeon is responsible for collecting data from MQ, doing some work and
 returning new data on the MQ.

First draft of Pigeon implementation:

* pigeon takes 10 messages from MQ
* checks the validity of the data
* pre-formats the data in Time-Series format
* returns the data on Mq
