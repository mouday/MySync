# -*- coding: utf-8 -*-
"""
数据同步

支持
MySQL -> Elasticsearch

"""

import argparse
import time
from pprint import pprint

from mysync.util.config_util import parse_config
from mysync.util.logger import logger
from mysync.util.method_util import get_method
from mysync.util.time_util import format_time


def parse_args():
    """解析参数"""
    # 初始化解析器
    parser = argparse.ArgumentParser()

    # 定义参数
    parser.add_argument("-c", "--config", help="配置文件路径")
    parser.add_argument("-t", "--table", help="表名")

    # 解析
    return parser.parse_args()


def main(args):
    config = parse_config(args)
    pprint(config)

    # 输入参数
    input_config = config['input']
    table = input_config['table']
    producer = input_config['producer']
    producer_method = get_method(producer)

    # 输出参数
    output_config = config['output']
    index_name = output_config['index']
    stdout = output_config['stdout']
    consumer = output_config['consumer']
    consumer_method = get_method(consumer)

    # 开始同步
    logger.debug(f"sync start ~ table: {table} -> index: {index_name}")
    start_time = time.time()

    # 生产-消费
    total = 0
    for rows in producer_method(config):
        consumer_method(config, rows)

        if stdout:
            pprint(rows)

        total += len(rows)

    # 输出同步结果
    total_time = time.time() - start_time

    logger.debug("*" * 20)
    logger.debug(f"sync end ~ table: {table} -> index: {index_name}")
    logger.debug(f"sync total: {total}")
    logger.debug(f"sync time: {format_time(total_time)}")
    logger.debug("*" * 20)


if __name__ == '__main__':
    main(parse_args())
