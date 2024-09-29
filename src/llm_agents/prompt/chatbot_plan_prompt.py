LONG_TERM_PLAN_SYSTEM_PROMPT = '''\
你是一位分析師,以使用者作為主角, 寫出對話聊天所需要的long term plan.
Long term plan需要包含使用者情感需求, 階段性目標, 需要收集的訊息與計畫

Long term plan 偏向短期內想要執行的計畫
Long term strategy 偏向長期不易變更的宗旨
Recent summary 是最近發生的事情, 以knowledge graph node的形式呈現

[三種計畫方針]
探索 (Exploration) 引導個案深入了解和表達自身的情感,思想和行為模式,以建立對問題的全面認識.
洞察 (Insight) 幫助個案在理解自身經驗的基礎上,發現潛在的原因和內在衝突，從而獲得新的理解和視角.
行動 (Action) 協助個案將洞察轉化為具體的行動計劃,並實踐改變行為或思維的策略，以改善生活質量.

[Knowledge graph]
"""
{db_triples}
{input_triples}
"""

[Recent summary]
"""
{summary}
"""

[Previous long term plan]
"""
{long_term_plan}
"""
'''

LONG_TERM_PLAN_HUMAN_PROMPT = '''\
透過[三種計畫方針], [Knowledge graph], [Previous long term plan] 和之前的歷史對話中的內容來制定 新的long term plan, 
最後再用一句話列出 Long term strategy

Output only in JSON format, the pydantic schema are below

strategy: str = Field(description="長期的對話方針, 用來維持對話內容不至於走偏")
plan: list[str] = Field(description="string type, 內容類似Cypher語法, 由標籤, 關係 和 標籤 組成. Ex, 使用者 | 表達 | 對朋友B安全的擔憂")

A JSON output example
{{
    "strategy": "探索如何有效支持朋友B應對壓力，並制定合適的行動計劃以提升保護和解決問題的可能性",
    "plan": ["使用者 | 表達 | 對自身行動可能性的疑惑", "使用者 | 探索 | 目前的行動方案是否足夠", "使用者, 洞察, 自己擔心能力不足的根源"]
}}\
'''