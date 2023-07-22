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


