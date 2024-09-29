RETRIVE_KG_SYSTEM_PROMPT = """\
我打算繪製一幅Knowledge graph, 而你是世上最好的關係分析師

請依照以下順序做事
1. 根據 '使用者回覆', 仔細思考 並分析整段話中 重要的訊息為何。
2. 將[Summary]作為輔助用的參考資料, 把 '使用者回覆' 和 '思考過程',  以Json 的方式呈現 使用者Knowledge Graph，

[Summary]
'''
{summary}
'''

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

KG_FILTERED_SYSTEM_PROMPT = """
I want you to pick the most relevant knowledge graph nodes from Past nodes compare to current nodes.
They should be relevant in context.

Pick no more than '{number}' most relevant nodes from past node
The format of knowledge node are in JSON format, and you need to strictly follow the rule.
{{
  "triples": [
     "string type, 內容類似Cypher語法, 由標籤, 關係 和 標籤 組成. Ex, Thomas | 朋友 | Thomas",
  ]
}}\
"""

KG_FILTERED_HUMAN_PROMPT = """
[past nodes]
'''
{retrieve_triples}
'''

[current nodes]
'''
{kg_triples}
"""


KG_SUMMARY_SYSTEM_PROMPT = """\
你是一位優秀的分析師，將"使用者Knowledge Graph"中的訊息, 重新彙整簡化使用者近況, 整理成"使用者近況Knowledge Graph".
使用者近況包含使用者的工作、學習、健康、人際關係、生活、財務狀況與個人目標，並彙整成triple的形式呈現。 
triple:(node, relation, node)
 
使用者近況 輸出規定: 使用者作為主角, 簡化使用者Knowledge Graph, 做成使用者近況Knowledge Graph, 
需包含以下七個部分, 如果沒有提則留白
**工作**: 職位,職責, 職業發展或目標, 是否參與新項目或擔責任 
**學習**: 是否有新學習計畫,學習進展,學習成果,是否出國 
**健康**: 身體機能,年齡,性別、體型,心理狀態,是否有身體缺陷 
**人際關係**: 家庭狀況,是否有配偶,有無子女,原生家庭,是否有家人生病,與朋友,同事,家人關係 
**生活**: 是否遇重大變故,有無旅遊規劃,興趣,是否發展新愛好,喜好
**財務狀況**: 收支,貸款,投資
**個人目標**: 近期目標,長期目標與近期目標是否相同\
"""

KG_SUMMARY_HUMAN_PROMPT = """\
[過去的近況]
'''
{summary}
'''

[使用者Knowledge Graph]
'''
{triples}
'''

請結合以上兩點, 並給出一份使用者近況Knowledge Graph\
不要超過20個Triple
"""

KG_UPSERT_SYSTEM_PROMPT = """
You are absolutely beast in field of knowledge graph, now I got two group of knowledge graphs node
One is the previous graph node and new coming node, I want you specified out which nodes from
previous graph node should be delete, given the new node will replace their state.

First shortly figure out which previous node you think need to be delete,
and output a JSON object with the schema I list below

delete_nodes: list[string] = Field(description='Previous ID that no longer need to exist, since the new node will replace them')
"""

KG_UPSERT_HUMAN_PROMPT = """
[previous graph node]
'''
{previous_nodes}
'''

[new coming nodes]
'''
{new_nodes}
'''
"""