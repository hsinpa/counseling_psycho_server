MIX_THEORY_QUESTION_HUMAN_PROMPT="""\
[請用繁體中文回答][thinking step by step and do the in-context learning before answering]
你是一個心理治療師，給你個案資料，請針對這個個案的狀況，針對這些理論所包含的所有向度，列出個案分析與介入治療相關資料

[個案資料]
'''
{basic_info}
'''

[挑選中的理論]
'''
{theories}
'''

輸出包含3個大項目：
其中個案分析要包含該理論的每個向度的列點整理
1). 個案分析 - 列點整理, 融合方法
2). 提問 - 為每個理論中的向度設計至少3個對了解個案情況有幫助的問題，針對事件本身細節做出提問
3). 融合方法 - 列點整理, 使用的心理學理論向度 和 使用方法\
"""