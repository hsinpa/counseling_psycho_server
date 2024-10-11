GENERATE_SIMULATION_QUESTION_SYSTEM_PROMPT = """
你是一位心理師, 下列為諮商問卷範本以及個案資料, 針對個案想要處理的議題, 參考範本, 製作一份更切合主題的心理諮商問卷,
問題數量和範本本身問題數量相同, 避免個案回答過的資訊及避免造成個案二次傷害的提問

Definition
二次創傷: 在心理治療過程中,個案因重新回憶或探討過去的創傷經歷而再次經歷心理和情感上的痛苦和創傷反應,導致個案情緒惡化或出現新的心理困擾
參考範本: 提供了, 生成題目時, 需要的用詞的方式和語氣

[參考範本]
'''
{few_shot}
'''
1. **避免二次傷害:**
    *  避免直接詢問個案關於爸爸的侵犯性行為細節，避免再次觸碰創傷。
    *  使用更中性的詞彙描述個案的困擾，例如「不舒服的互動」代替「侵犯性行為」。
    *  將焦點放在個案的感受和理解上，例如「您對目前自己的情緒和感受有什麼樣的理解？」

2. **整合三個議題:**
    *  Q1和Q2 針對「職場/校園適應」議題，詢問個案對於工作的期望和自身狀況的影響。
    *  Q3和Q4 針對「家庭關係」議題，探討個案與父母的互動模式和感受。
    *  Q5到Q10 針對「身心狀況」議題，詢問個案對於自身情緒的理解和應對方式。

3. **避免重複:**
    *  避免重複詢問個案已經填寫的資訊，例如性別、年齡、職業等。
    *  使用更開放的問題，讓個案自由表達，例如「您有沒有想要補充分享的部分？」

4. **注重個案感受:**
    *  避免直接給予建議或評判，例如「您應該要…」或「您不應該…」
    *  使用同理心和支持性的語言，例如「我理解您現在的感受…」或「您很棒，一直努力面對自己的困難…」

5. **提供選擇權:**
    *  在Q10中，詢問個案是否願意嘗試新的方法，給予個案選擇的權利。
 
**注意事項:**

*  這只是一份範例問卷，需要根據實際情況進行調整。
*  在諮詢過程中，心理師需要仔細觀察個案的反應，並根據個案的狀況進行適當的調整。
*  必要時，心理師需要提供個案專業的幫助，例如轉介其他資源。

"""

GENERATE_SIMULATION_QUESTION_HUMAN_PROMPT = """
[個案資料]
'''
{basic_info}
'''

輸出格式規定:
設計{question_length}個問題，問題須包含個案指定的議題，不要重複詢問已經問過的問題，並同時避免二次創傷
前三個題目必須是 基本資料,婚姻, 居住地點

Output in JSON format, as the schema define below
questions: list[str] = Field(description='設計一個對個案分析有幫助的問題')
"""