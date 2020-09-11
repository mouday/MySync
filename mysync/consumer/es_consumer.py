# -*- coding: utf-8 -*-
from elasticsearch import Elasticsearch
from mysync.util.es_util import ESUtil
from mysync.util.logger import logger

SINGLE_ES = None


def get_elasticsearch(es_config):
    global SINGLE_ES

    if not SINGLE_ES:
        SINGLE_ES = Elasticsearch(**es_config)

    return SINGLE_ES


def consumer(config, rows):
    """数据消费者"""
    output_config = config['output']
    es_config = output_config['elasticsearch']
    index_name = output_config['index']
    document_type = output_config['document_type']
    document_id = output_config['document_id']

    es = get_elasticsearch(es_config)

    body = ESUtil.encode_doc(index_name, document_type, document_id, rows)
    es.bulk(body)
    logger.debug('elasticsearch success')
