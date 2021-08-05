

![Docker Hub](https://img.shields.io/badge/Capstone%20Project-Data%20Engineering-lightgrey?style=for-the-badge&logo=appveyor)
# Zomato Sales & Rating Data Warehouse

The goal of this project was to create a robust, feature-packed Data Warehouse by  using all the techiniques learnt in Udacity's Data Engineering Nanodegree program. This project underscores almost all the major components of the aforementioned degree. The dataset for this project can be found from this [link](https://www.kaggle.com/himanshupoddar/zomato-bangalore-restaurants). A light and altered version of this dataset is available here for a quick peak where the column names have been eased.

![zomato](https://cityspideynews.s3.amazonaws.com/uploads/spidey/202104/zomato-1619519108.png)
### Scope of the Project
The current project can be used to track the aggregate and average rating of any individual restaurant. On what rating people are spending average amount of money. This analysis can help businesses to take informed decisions and adopt strategies based on the results.

The data can be used by business analysts to help in deciding the strategies. The aspiring entrepreneurs, which type of restaurants are performing well and what should be their new restaurant type if they want to open one. By chefs, what dishes are being more liked. 
A chef (potential user) can do so by the following steps:
- Choose a restaurant and find its ratings and sort them in `DESC` order
- Get the `dish_liked` column and analyze them


### Architecture
![docker postgres redis airflow](https://miro.medium.com/max/1052/1*JQUBRf6OscKNdrXpk8XTfQ.png)

We are using a fully managed version of the Airflow inside of docker, jam-packed with Redis, Postgres and a pool of Airflow workers. We used [Amazon S3](https://aws.amazon.com/s3/) to store our dataset and [Amazon Redshift](https://aws.amazon.com/redshift/) to store a relational version of our dataset.

#### Why using these technologies?
- It's a good question. Since we have a plethora of technologies, it is critical for us to choose a technology consciously, knowing it's pros and cons. I used [Amazon S3](https://aws.amazon.com/s3/) because it offers industry-leading scalability, data availability, security, and performance all in one place. 

- The decision of using Apache Airflow is two folds. One, we need to ingest data on a daily basis so we had to choose a scheduling framework or maybe just raw crontabs. Since, Airflow is a known, battle-tested piece of tech so I got more inclined towards it. Secondly, we didn't need much processing with the data and raw python was enough so Airflow was perfect for this.

- Dockerizing the whole system was inevitable. It's very easy to get up and running with containerized applications because it guarantees easy setup, deployment and consistent results.

### Data Modeling
This warehouse consists of 3 dimensional tables, 1 fact table and one staging table. Schemas are given below:

#### Staging table

##### TABLE staging_restaurants
~~~
root
|-- url: VARCHAR(2048)
|-- address: VARCHAR(512)
|-- name: VARCHAR(256)
|-- online_order: VARCHAR(8)
|-- book_table: VARCHAR(8)
|-- rate: VARCHAR(256)
|-- votes: VARCHAR(256)
|-- phone: VARCHAR(64)
|-- location: VARCHAR(512)
|-- rest_type: VARCHAR(256)
|-- dish_liked: VARCHAR(512)
|-- cuisines: VARCHAR(256)
|-- approx_cost_for_two_people: VARCHAR(256)
|-- listed_in_type: VARCHAR(64)
|-- listed_in_city… VARCHAR(64)
~~~

#### Dimension tables

##### TABLE restaurants

~~~~
root
|-- id: INT IDENTITY(1,1) PRIMARY KEY
|-- name: VARCHAR(256)
|-- url: VARCHAR(2048)
|-- address: VARCHAR(512)
|-- phone: VARCHAR(64)
|-- location: VARCHAR(256)
|-- rest_type: VARCHAR(256)
|-- listed_in_type: VARCHAR(64)
|-- listed_in_city: VARCHAR(64)
|-- cuisines: VARCHAR(256)
~~~~

##### TABLE orders

~~~~
root
|-- id: INT IDENTITY(1,1) PRIMARY KEY
|-- online_order: BOOL
|-- book_table: BOOL
|-- dish_liked: VARCHAR(512)
|-- url: VARCHAR(2048)
~~~~

##### TABLE ratings

~~~~
root
|-- id: INT IDENTITY(1,1) PRIMARY KEY
|-- votes: INT4
|-- rating: NUMERIC
|-- url: VARCHAR(2048)
~~~~

#### Fact table

##### TABLE sales

~~~~
root
|-- id: INT IDENTITY(1,1) PRIMARY KEY
|-- restaurant_id: INT4
|-- rating_id: INT4
|-- order_id: INT4
|-- cost: NUMERIC
~~~~

### ERD
![erd](https://imgur.com/kJOQGNr.png)

#### About the schema
The initial staging has all the `VARCHAR` fields because data is in crude form. For example, the rating was present as `4.1/5` so we extracted the proper rating with the help of our SQL. One noteworthy thing, the column names were a bit difficult to comprehend by the database so we normalised them by preprocessing it. Some column names had special characters and spacing

--------------------------------------------
### How to run the project?
- Make sure you have [docker](https://www.docker.com/products/docker-desktop) installed 
- Clone this repository
- In the root folder of this project, run the following command in terminal with docker running in background. This command will take some time depending upon your internet connection
	```python
	docker-compose up airflow_init
	```
- After completion of the above command, run the following
	```python
	docker-compose up
	```
- Now upload the dataset on [Amazon S3](https://aws.amazon.com/s3/) and take care of two things. First, make sure it's publicly available or otherwise, you'll need to tweek the settings in the code. Second, it's in the same region where you'll be launching your  [Amazon Redshift](https://aws.amazon.com/redshift/) cluster.
- Now launch a  [Amazon Redshift](https://aws.amazon.com/redshift/) cluster. I used a `dc2.large` cluster with 4 nodes
- Go to localhost:8080 to your Airflow instance and add a connection named `redshift` and another connection `aws_credentials`
- Add the s3 dataset link in the code file `zomato_pipeline.py`
- Now all you need to do is go to DAGs > zomato_pipeline and run the DAG.
- Great Job! 😃

### Outputs
The successful run of DAG looks like the following:
#### DAG Graph View
![img](https://i.imgur.com/nZe5izg.png)
#### DAG Tree View
![dag flow](https://i.imgur.com/QCROJcS.png)
#### DAG Gantt Chart View
![Imgur](https://imgur.com/GNNnVc1.png)
### Scenarios
- ####  If the data was increased by 100x.
	- Sounds like a perfect job for Spark because of its distributed architecture. It can handle it without sweating
	- We can introduce EMRs to handle large amounts of data with a fully organized ecosystem. The Amazon S3 can be deployed to handle very large amounts of data.
	- Partitioning can be helpful but we are seeing that we don't have very large updates happening at a single time or any table has larger number of records than any other table so partitioning might be suitable right away.
- ####  If the pipelines were run on a daily basis by 7am.
	- This can easily be handled by using Apache Airflow and setting a daily interval to 7 AM. We can also provide a crontab syntax of `0 7 * * *` in the `schedule_interval` argument of the `DAG`
	- This can definitely increase the operational costs. Since we are using Amazon, managing the resources won't be an issue on our side but it bills will hike
	- It is a good idea to have a separate instance for Airflow so if it fails, it doesn't effect any other of our business processes
- #### If the database needed to be accessed by 100+ people
	- We can tackle this problem with Amazon Redshift due to its nature. Amazon guranatees its high availability, fault taulerant and accessibility. Moreover, we can use Hive as well.
	- Although, Redshift can be used by upto 100 people at max to access the snapshots. We can manage the query time of multiple people and this can also be taken care of
	- Since more people are using the accounts, this will definitely hike our bill too. But the cost is justified because handling all this infrastructure on-premises would be much more costly.


Thank you so much. It was a wonderful experience.
