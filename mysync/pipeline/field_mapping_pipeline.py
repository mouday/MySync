# -*- coding: utf-8 -*-


def pipeline(config, rows):
    """字段映射处理器"""
    field_mapping = config['pipeline']['field_mapping']

    if not field_mapping:
        return

    for row in rows:
        for old_key, new_key in field_mapping.items():
            value = row.pop(old_key)
            row[new_key] = value


def main():
    config = {
        "pipeline": {
            "field_mapping": {
                "old_key": "new_key"
            }
        }
    }

    data = [
        {
            "key": "value",
            "age": 23
        }
    ]

    pipeline(config, data)
    print(data)


if __name__ == '__main__':
    main()
