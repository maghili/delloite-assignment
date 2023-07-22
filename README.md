# Solution
We can write a service that is composed of two microservices `api`, and `daemon`. The api microservice will handle the requests of what files need to be processed and can scale based on the number of requests and the daemon miroservice will do the actual processing of the data and can scale based on the resource usage.

To handle the file, we can create our own file management `bucket.py` so we can unify local (for development) and cloud solutions. 

The file cleaning can contain some checks and balances on the format of the email field, and on the validity of the ip address using regex for example (`([0-1][0-9]+|2[0-4][0-9]|25[0-5]).([0-1][0-9]+|2[0-4][0-9]|25[0-5]).([0-1][0-9]+|2[0-4][0-9]|25[0-5]).([0-1][0-9]+|2[0-4][0-9]|25[0-5])`)

The 