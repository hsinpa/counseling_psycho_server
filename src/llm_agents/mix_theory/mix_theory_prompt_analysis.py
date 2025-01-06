MIX_THEORY_ANALYSIS_HUMAN_PROMPT = """\
你是一名專業的心理師，請根據以下個案資料，將選定的理論融合，並將不同理論中，類似觀點的向度進行融合，做個案融合理論分析

[個案資料]
'''
{basic_info}
'''

[挑選中的理論]
'''
{theories}
'''

[專有名詞解釋]
'''
理論融合視角: 綜合多種理論和方法，以全面理解和解釋複雜的心理現象
互補作用: 不同因素互相補充，彌補彼此的不足，進而提升整體效果
協同作用: 多個因素共同作用時所產生的效果大於各自單獨作用效果的總和
交互作用: 一個因素的效應依賴另一個因素的層次或狀態
調節作用: 一個變因影響另一個變項對結果的效果
'''

輸出規定: 須包含5個項目 

1). 融合的理論: 來自[挑選中的理論]
使用的理論向度: 列點向度與應用方式

2). 不同理論的向度的融合方式:
詳述融合的方法: 透過理論融合視角、互補作用、交互作用、協同作用、調節作用等面向，用1000字詳細敘述三種理論的融合方法與步驟

3). 個案狀態分析: 針對個案狀態做2000字個案狀態作質性分析

4). 融合理論分析: 整合三種理論的角度，針對個案治療目標、兼容理論觀點、各個理論對於本個案的治療優勢面向與融合治療的方法與優勢、方法兼容與實施步驟建議，靈活將三種理論融合，並用2000字闡述整合報告
前期: 列點融合分析方法與步驟兼容
中期: 列點融合分析方法與步驟兼容
後期: 列點融合分析方法與步驟兼容

5). 治療目標與預計達成成效\
"""