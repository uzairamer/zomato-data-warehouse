from datetime import datetime

from airflow import DAG
from airflow.operators.dummy_operator import DummyOperator

from helpers import SQLQueries
from operators import (
    CopyToRedshiftOperator,
    DataQualityOperator,
    DropTableOperator,
    LoadFactOperator,
    LoadDimensionOperator,
)


dag = DAG(
    "zomato_pipeline",
    start_date=datetime.now(),
)

start_operator = DummyOperator(task_id="Begin_execution", dag=dag)

drop_table_staging_restaurants = DropTableOperator(
    task_id="drop_table_staging_restaurants",
    dag=dag,
    redshift_conn_id="redshift",
    table_name="public.staging_restaurants"
)

drop_table_sales = DropTableOperator(
    task_id="drop_table_sales",
    dag=dag,
    redshift_conn_id="redshift",
    table_name="public.sales"
)

drop_table_restaurants = DropTableOperator(
    task_id="drop_table_restaurants",
    dag=dag,
    redshift_conn_id="redshift",
    table_name="public.restaurants"
)

drop_table_orders = DropTableOperator(
    task_id="drop_table_orders",
    dag=dag,
    redshift_conn_id="redshift",
    table_name="public.orders"
)

drop_table_ratings = DropTableOperator(
    task_id="drop_table_ratings",
    dag=dag,
    redshift_conn_id="redshift",
    table_name="public.ratings"
)

copy_to_redshift = CopyToRedshiftOperator(
    task_id="Copy_staging_data_to_redshift_instance",
    dag=dag,
    table_name="public.staging_restaurants",
    redshift_conn_id="redshift",
    aws_credentials_id="aws_credentials",
    s3_path="<INSERT-FULL-QUALIFIED-S3-DATASET-PATH>",
    data_type="CSV",
    create_table_sql=SQLQueries.create_staging_restaurants_table,
)

load_restaurants_table = LoadDimensionOperator(
    task_id="Load_restaurants_dimension_table",
    dag=dag,
    redshift_conn_id="redshift",
    create_statement_table=SQLQueries.create_restaurant_table,
    sql=SQLQueries.restaurants_table_insert,
)

load_orders_table = LoadDimensionOperator(
    task_id="Load_orders_dimension_table",
    dag=dag,
    redshift_conn_id="redshift",
    create_statement_table=SQLQueries.create_orders_table,
    sql=SQLQueries.orders_table_insert,
)

load_ratings_table = LoadDimensionOperator(
    task_id="Load_ratings_dimension_table",
    dag=dag,
    redshift_conn_id="redshift",
    create_statement_table=SQLQueries.create_ratings_table,
    sql=SQLQueries.ratings_table_insert,
)

load_sales_table = LoadFactOperator(
    task_id="Load_sales_fact_table",
    dag=dag,
    redshift_conn_id="redshift",
    create_statement_table=SQLQueries.create_sales_table,
    sql=SQLQueries.sales_table_insert,
)

test_restaurants = DataQualityOperator(
    task_id="Quality_check_for_restaurants",
    dag=dag,
    redshift_conn_id="redshift",
    test_cases=[(SQLQueries.restaurants_count_test, 0)],
)

test_sales = DataQualityOperator(
    task_id="Quality_check_for_sales",
    dag=dag,
    redshift_conn_id="redshift",
    test_cases=[(SQLQueries.sales_count_test, 0)],
)

test_orders = DataQualityOperator(
    task_id="Quality_check_for_orders",
    dag=dag,
    redshift_conn_id="redshift",
    test_cases=[(SQLQueries.orders_count_test, 0)],
)

test_ratings = DataQualityOperator(
    task_id="Quality_check_for_ratings",
    dag=dag,
    redshift_conn_id="redshift",
    test_cases=[(SQLQueries.ratings_count_test, 0)],
)

end_operator = DummyOperator(task_id="Stop_execution", dag=dag)


start_operator >> drop_table_staging_restaurants >> copy_to_redshift
start_operator >> drop_table_sales >> copy_to_redshift
start_operator >> drop_table_restaurants >> copy_to_redshift
start_operator >> drop_table_orders >> copy_to_redshift
start_operator >> drop_table_ratings >> copy_to_redshift

copy_to_redshift >> load_restaurants_table >> test_restaurants >> end_operator
copy_to_redshift >> load_orders_table >> test_orders >> end_operator
copy_to_redshift >> load_ratings_table >> test_ratings >> end_operator
copy_to_redshift >> load_sales_table >> test_sales >> end_operator
