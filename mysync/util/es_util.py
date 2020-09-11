# -*- coding: utf-8 -*-
import json

from mysync.util.json_encoder import JSONEncoder


class ESUtil(object):
    @staticmethod
    def encode_doc(index_name, document_type, document_id, rows):
        """组装json数据"""

        doc_list = []

        for row in rows:
            header = {"index": {"_index": index_name, "_type": document_type, "_id": row[document_id]}}

            doc_list.append(json.dumps(header, ensure_ascii=False))
            doc_list.append(json.dumps(row, ensure_ascii=False, cls=JSONEncoder))

        return "\n".join(doc_list)
