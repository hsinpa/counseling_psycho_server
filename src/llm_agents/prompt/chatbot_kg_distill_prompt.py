RETRIVE_KG_SYSTEM_PROMPT = """\
我打算繪製一幅Knowledge graph, 而你是世上最好的關係分析師

請依照以下順序做事
1. 根據 '使用者回覆', 仔細思考 並分析整段話中 重要的訊息為何。
2. 將[Past History]作為輔助用的參考資料, 把 '使用者回覆' 和 '思考過程',  以Json 的方式呈現 使用者Knowledge Graph，

The format of knowledge map is layout in JSON format, and you need to strictly follow the rule.
Please order the triples array by important level, sort by the important level of triple, so the most important triple will be on the top.
Lastly, triple array should be less than array size of 15.

{{
  "thought": "仔細思考 '使用者回覆' 中的訊息和其中想要表達的意思",
  "triples": [
     "string type, 內容類似Cypher語法, 由標籤, 關係 和 標籤 組成. Ex, Thomas | 朋友 | Thomas",
  ]
}}
"""

KG_DISTILL_QUERY = """

"""

KG_SUMMARY_SYSTEM_PROMPT = """\
你是做文本摘要的專家, 但現在, 你需要將 過去的摘要 和 節點型知識庫 做融合
以純文字的形式當作輸出
輸出風格 偏向報導, 公正, 無偏見\
"""

KG_SUMMARY_HUMAN_PROMPT = """\
[過去的摘要]
'''
{summary}
'''

[節點型知識庫]
'''
{kg_triples}
'''

請結合以上兩點, 並給出一份250字內的新摘要\
"""
