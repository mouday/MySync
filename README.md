# MySync

同步MySQL数据到ElasticSearch

支持全量同步

必须有自增id

安装
```bash
$ pip install mysync

$ mysync

# run config test 
$ mysync -t config.yml

# run sync
$ mysync -c config.yml
```

默认的配置文件default_config.yml
```yml
# 输入配置
input:

  # 数据库配置
  mysql:
    db_url: ~

    # 或者
    host: '127.0.0.1'
    port: 3306
    database: data
    username: root
    password: ''

  # 主键列名
  primary_key: id

  # 主键类型
  primary_type: int

  # 同步的表名，必填
  # table: ''

  # 需要同步字段
  fields: '*'

  # 分页大小
  size: 10

  # 生产者，会按照路径导入
  producer: 'mysync.producer.mysql_producer@producer'

  # 启用同步点
  sync_point: true

  # 同步点文件
  sync_file: ~

# 数据处理管道
pipeline:
  handlers: ~

# 输出配置
output:

  # ES配置
  elasticsearch:
    hosts:
      - 'http://127.0.0.1:9200'

  # 索引名，必填
  # index: ''

  # 操作：index, update
  action: 'index'

  # 文档type
  document_type: 'doc'

  # 文档id
  document_id: 'id'

  # 是否在控制台输出json
  stdout: false

  # 数据消费者
  consumer: 'mysync.consumer.es_consumer@consumer'

```

默认的处理器
```
# 生产者，会按照路径导入
producer: 'mysync.producer.mysql_producer@producer'

# 数据消费者
consumer: 'mysync.consumer.es_consumer@consumer'

# 可选的数据处理器
handlers: 
    - mysync.pipeline.field_mapping_pipeline@pipeline

```

接口说明
```
生产者
def producer(config):

处理器
def pipeline(config, rows)

消费者
def consumer(config, rows):
```

## TODO

~~1. 配置文件继承 `extends`~~
~~2. 配置文件运行前检测 `-t`~~

