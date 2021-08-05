from airflow.hooks.postgres_hook import PostgresHook
from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults


class LoadDimensionOperator(BaseOperator):
    ui_color = "#80BD9E"

    @apply_defaults
    def __init__(
        self, redshift_conn_id="", create_statement_table="", sql="", *args, **kwargs
    ):

        super(LoadDimensionOperator, self).__init__(*args, **kwargs)
        self.redshift_conn_id = redshift_conn_id
        self.create_statement_table = create_statement_table
        self.sql = sql

    def execute(self, context):
        redshift = PostgresHook(postgres_conn_id=self.redshift_conn_id)
        self.log.info(f'Creating table with sql: {self.create_statement_table}')
        redshift.run(self.create_statement_table)

        self.log.info(f'Inserting into table with sql: {self.sql}')
        redshift.run(self.sql)
