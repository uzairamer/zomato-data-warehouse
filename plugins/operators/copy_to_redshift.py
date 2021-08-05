import logging

from airflow.hooks.postgres_hook import PostgresHook
from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults
from airflow.contrib.hooks.aws_hook import AwsHook


class CopyToRedshiftOperator(BaseOperator):
    ui_color = "#358140"
    _sql = """
        COPY {}
        FROM '{}'
        ACCESS_KEY_ID '<INSERT-ACCESS-KEY>'
        SECRET_ACCESS_KEY '<INSERT-SECRET-KEY>'
        region 'us-west-2'
        {}
        IGNOREHEADER 1;
    """

    @apply_defaults
    def __init__(
        self,
        table_name="",
        s3_path="",
        data_type="",
        redshift_conn_id="",
        aws_credentials_id="",
        create_table_sql="",
        *args,
        **kwargs,
    ):
        super().__init__(*args, **kwargs)

        self.table_name = table_name
        self.s3_path = s3_path
        self.data_type = data_type
        self.redshift_conn_id = redshift_conn_id
        self.aws_credentials_id = aws_credentials_id
        self.create_table_sql = create_table_sql

    def execute(self, context):
        # aws_hook = AwsHook(aws_conn_id=self.aws_credentials_id)
        # credentials = aws_hook.get_credentials()
        # logging.info(credentials)

        formatted_sql = self._sql.format(
            self.table_name,
            self.s3_path,
            # credentials.access_key,
            # credentials.secret_key,
            self.data_type
        )

        logging.info(f'Creating table with sql: {self.create_table_sql}')
        redshift = PostgresHook(postgres_conn_id=self.redshift_conn_id)
        redshift.run(self.create_table_sql)
        logging.info('Copying data to redshift')
        redshift.run(formatted_sql)
