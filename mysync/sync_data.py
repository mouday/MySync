# -*- coding: utf-8 -*-
"""
数据同步

支持
MySQL -> Elasticsearch

"""
import os
import sys

base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, base_dir)
# print(sys.path)

import argparse
import time
from pprint import pprint

from mysync.util.config_util import parse_config, init_config
from mysync.util.logger import logger
from mysync.util.method_util import get_method
from mysync.util.time_util import format_time
from mysync.version import VERSION


def parse_args():
    """解析参数"""
    # 初始化解析器
    parser = argparse.ArgumentParser()

    # 定义参数
    parser.add_argument("-c", "--config", help="配置文件路径")
    parser.add_argument("-t", "--table", help="表名")

    # 解析
    return parser.parse_args()


def start_sync(args):
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
    logger.debug(f"sync table: {table} -> index: {index_name}")
    logger.debug(f"sync total: {total}")
    logger.debug(f"sync time: {format_time(total_time)}")
    logger.debug("*" * 20)


def main():
    if len(sys.argv) == 1:
        print("mysync version", VERSION)
        print("$ mysync -h : show mysync help")

    elif len(sys.argv) == 2:
        action = sys.argv[1]
        if action == 'init':
            init_config()
        elif action == 'version':
            print("version", VERSION)
        elif action == '-h':
            print("$ mysync init : generator a default config file")
            print("$ mysync version : show mysync version")
            print("$ mysync -t <table_name> : run a sync action from table config")
            print("$ mysync -c <config_path> : run a sync action from config path")

    else:
        start_sync(parse_args())


if __name__ == '__main__':
    main()
