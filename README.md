# Solution
I made a mistake with the time i chose for this project but with the very little time i have here is how I would have proceeded.

We can write a service that is composed of two microservices `api`, and `daemon`. The api microservice will handle the requests of what files need to be processed and can scale based on the number of requests and the daemon miroservice will do the actual processing of the data and can scale based on the resource usage.

To handle the file, we can create our own file management `bucket.py` so we can unify local (for development) and cloud solutions. We can also create our own version of logging and our own version of connction to the dbs to make it compatible for our design.

The file cleaning can contain some checks and balances on the format of the email field, and on the validity of the ip address using regex for example (`([0-1][0-9]+|2[0-4][0-9]|25[0-5]).([0-1][0-9]+|2[0-4][0-9]|25[0-5]).([0-1][0-9]+|2[0-4][0-9]|25[0-5]).([0-1][0-9]+|2[0-4][0-9]|25[0-5])`)

The data then can be divided into three tables: person, person_ip, and gender

```sql
create table person (
id serial primary key,
name varchar,
lastname varchar,
email varchar,
gender_id int,
constraint email_u unique (email)
);
```
```sql
create table person_ip (
	user_id int,
	ip varchar,
    constraint user_id_ip_u unique(user_id, ip)
);
```

```sql
create table gender (
id serial primary key,
gender_type varchar,
constraint gender_type_u unique (gender_type)
);
```
```sql
insert into gender (gender_type) 
values ('genderfluid'),
('bigender'),
('male'),
('non-binary'),
('female'),
('agender'),
('genderqueer'),
('polygender');
```


Then we can upsert the data, i.e. insert and on conflict update.

Creating a dockerfile, would be very good for the containerization of the code, and then the deployment to kubernetes in which we can set the horizontal pod scaling policy.

A terraform file that contains the creation of the required assets such as the postgres instance would be very good in this case.


# Questionare


1. What is a Data Lake? Explain its benefits, how it differs from a data warehouse, and how it might benefit a client.
    A data lake is usually the storage that is used for the files and raw data, and a datawarehouse is usually a sql or nosql where the data is kept in the format to be used for the application purposes. data warehouse allows one to draw insight out of the data and it should be designed according to the rquirements of the project
2. Explain serverless architecture. What are its pros and cons?
    Serverless architecture such as dataflow in GCP are very benefitial if one needs to run the pipeline with minimal amount of maintenance of the infrastructure. The pro is that you get a solution out of the box with minimal maintenance and the con is that one does not have as much flexibility with it to costomize it towards what one needs and therefore it might be a little bit hard to deal with for customization.
3. Please provide a diagram for an ETL pipeline (e.g., Section 2) using serverless AWS services. Describe each component and its function within the pipeline.
    Since I have more experience with GCP I will do this with that. I will use the dataflow that would read the data and would apply some cleaning on it and outputs the data in BQ. both these services are serverless and do not need any maintenance and they would give you out of the box logging and monitoring.
4. Describe modern MLOps and how organizations should be approaching management from a tool and system perspective.
    
