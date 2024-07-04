INDIVIDUAL_THEORY_REPORT_PROMPT = """\
根據以下治療師的問題與個案的回答，以其客體關係中:'家庭背景和成長環境'、'目前狀況和生活狀態'、'心理病史和治療歷程'、'自我認知和情感狀態'、'關係模式、'自我──客體關係'的概念，
提供我5000字的個案心理狀態分析，並列點呈現且詳細說明各項目內容。

'''
{content}
'''\
"""

MEDIATION_STRATEGY_REPORT_PROMPT = """\
根據以下個案的資料，提供我使用客體關係理論概念進行的5000字詳細治療策略，請用列點的方式呈現，並根據列點後的每個項目再進行更詳細的說明。

'''
{content}
'''\
"""

COGNITIVE_BEHAVIOR_REPORT_PROMPT = """\
你是一名專業的心理師，請根據以下心理師的問題與個案的回答，認知行為療法(Cognitive Behavioral Therapy)中: 
'核心信念(core beliefs)','中介信念(assumptions)','因應策略(coping strategies)', '促發情境(situation)', '自動化思考(automatic thoughts)','身心反應(reaction)'，
提供我5000字的個案心理狀態分析，並列點呈現且詳細說明各項目內容

'''
{user_content}
'''
"""

USER_INFO_TEXT = """\
用戶性別: {gender}
年紀: {age}
會談主題: {theme}
會談期待: {expect}"""

THEORY_REPORT_TEXT = """\
心理師問題: {question}
用戶回答: {user_answer}"""