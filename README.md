![Docker Hub](https://img.shields.io/badge/Capstone%20Project-Data%20Engineering-lightgrey?style=for-the-badge&logo=appveyor)
# Zomato Sales & Rating Data Warehouse

The goal of this project was to create a robust, feature-packed Data Warehouse by  using all the techiniques learnt in Udacity's Data Engineering Nanodegree program. This project underscores almost all the major components of the aforementioned degree. The dataset for this project can be found from this [link](https://www.kaggle.com/himanshupoddar/zomato-bangalore-restaurants). A light and altered version of this dataset is available here for a quick peak where the column names have been eased.

![zomato](https://cityspideynews.s3.amazonaws.com/uploads/spidey/202104/zomato-1619519108.png)

To yield better understanding, I'll be walking you through each and every step.
### Architecture
![docker postgres redis airflow](https://miro.medium.com/max/1052/1*JQUBRf6OscKNdrXpk8XTfQ.png)

We are using a fully managed version of the Airflow inside of docker, jam-packed with Redis, Postgres and a pool of Airflow workers. We used [Amazon S3](https://aws.amazon.com/s3/) to store our dataset and [Amazon Redshift](https://aws.amazon.com/redshift/) to store a relational version of our dataset.

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
partitionBy("year", "artist_id")

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
|-- sale_id: INT4
|-- cost: NUMERIC
~~~~

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
- ####  If the pipelines were run on a daily basis by 7am.
	- This can easily be handled by using Apache Airflow and setting a daily interval to 7 AM. We can also provide a crontab syntax of `0 7 * * *`
- #### If the database needed to be accessed by 100+ people
	- We can tackle this problem with Amazon Redshift due to its nature. Amazon guranatees its high availability, fault taulerant and accessibility. Moreover, we can use Hive as well.


Thank you so much. It was a wonderful experience.
