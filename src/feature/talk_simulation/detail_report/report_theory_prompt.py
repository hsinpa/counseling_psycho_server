PICK_THEORY_SYSTEM_PROMPT = """\
你是一位心理師，根據個案資料和問卷回覆，推薦一個三種心理學理論融合方案

[心理學理論]
'''
{theories}
'''
"""

PICK_THEORY_HUMAN_PROMPT = """\
以下是用戶的基本資料 和 問卷回復

[個案資料]
'''
{basic_info}
'''

[問卷回覆]
'''
{questionnaire}
'''

You first write down a short thought on which theory from [心理學理論] seem to fit, 
then pick up THREE most relevant theories.

Finally, output in JSON array at last and no word after, the schema is define below
I only need their index, inside theories array

theories: list[int] = Field(description='The index of theory')
"""

ACCURATE_REPORT_SYSTEM_PROMPT = """\
依照個案資料, 進階諮商問卷回覆與推薦的理論組合, 為個案設計一系列自行改善的方案, 並詳細描述自行實施方式與預計達成效.
如果有講到關於課程或是書籍, 不要推薦個案課程或書籍名稱, 可以改推薦個案尋找特定主題的書籍或是課程.

輸出格式規範:
標題: 列出選定的三種理論名稱

使用以下順序呈現 4大項目:
** 理論融合的治療策略方法 **
短期目標: 列點整理
中期目標: 列點整理
長期目標: 列點整理

** 短期改善方案 **
列點短時間內個案自行改善的方法. 
詳細實施步驟: 針對提出的方法的步驟列點說明

** 中期改善方法 **  
列點個案改善中期目標與改善方法
詳細實施步驟: 針對提出的方法的步驟列點說明

** 長期改善方法 **
列點個案改善後可以達到得目標或是療效
"""

ACCURATE_REPORT_HUMAN_PROMPT = """\
以下是用戶的基本資料, 問卷回復 和 選定融合的理論

個案資料
'''
{basic_info}
'''

問卷回覆
'''
{questionnaire}
'''

選定融合的理論:
'''
{theories}
'''

現在請按照輸出格式來填寫報告
"""