# -*- coding: utf-8 -*-
from myquery import DataBase
from myquery.util.sql_builder_util import SQLBuilderUtil

from mysync.util.collection_util import Collection
from mysync.util.logger import logger
from mysync.util.sync_util import SyncUtil
import logging

query_logger = logging.getLogger("myquery")
query_logger.setLevel(logging.INFO)


def producer(config):
    """数据生产者，可以覆写此方法"""

    input_config = config['input']
    output_index = config['output']['index']

    # 输入参数
    mysql_config = input_config['mysql']

    table = input_config['table']
    fields = input_config['fields']

    if isinstance(fields, list):
        fields = SQLBuilderUtil.get_key_str(fields)

    sync_point = input_config['sync_point']
    sync_file = input_config['sync_file']
    primary_key = input_config['primary_key']
    primary_type = input_config['primary_type']
    size = input_config['size']

    # 支持断点续传
    if not sync_file:
        sync_file = f"{table}-{output_index}.txt"

    sync_util = SyncUtil(sync_file, primary_type)

    last_id = sync_util.read_sync_id(sync_point)

    sql = f"SELECT {fields} FROM {table} WHERE {primary_key} > %(id)s ORDER BY {primary_key} ASC limit %(size)s"

    db = DataBase(**mysql_config)

    while True:
        sync_util.write_sync_id(last_id)

        rows = db.select(sql, {"id": last_id, "size": size})

        if not rows:
            db.close()
            break

        last_id = Collection(rows).max("id")
        logger.debug(f"last_id {last_id}")

        yield rows
