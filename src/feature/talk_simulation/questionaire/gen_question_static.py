from src.feature.talk_simulation.talk_simulation_type import QuestionType, QuestionTypeEnum

LAST_QUESTION="""
請填寫您的基本資料,包含性別,年齡,婚姻,教育程度,職業,居住地點.
您覺得您是一個怎樣的人? 請簡單自我介紹一下, 像是您的個性怎麼樣, 身邊的人通常怎麼形容自己等等.
您的家庭關係如何?像是誰跟您住一起, 家人的工作, 您跟誰比較好, 彼此怎麼互動等等.
您目前最有意願, 最想要優先處理的狀況是什麼? 這個狀況從甚麼時候開始出現? 目前的頻率, 強度為何?
承上, 您怎麼看待這個狀況?
承上, 您採取什麼行為去應對這個狀況?
承上, 這個狀況帶給您什麼心理上的感受?
承上, 這個狀況帶給您什麼生理上的變化?
您身邊有哪些人可以支持您? 心事有人說嗎? 或是您有沒有參與什麼社團或信仰團體?
您過去有接受過心理諮商, 心理治療或就診身心科嗎?如果有的話那(幾)次的經驗怎麼樣?又是因為什麼原因而去的呢?

具體範例
Q1: 請您描述一下您理想中的工作環境和工作內容, 以及您希望在工作中獲得什麼?
Q2: 您認為目前您的身心狀況對您找工作造成了哪些影響?
Q3: 您覺得跟媽媽相處時, 哪些事情讓您感到不被愛? 您嘗試過哪些方式來獲得媽媽的愛?
Q4: 您能描述一下您跟爸爸的互動模式嗎? 哪些互動讓您感到不舒服?
Q5: 除了媽媽的偏愛和爸爸的行為, 還有哪些因素影響您對家庭的感受?
Q6: 您對目前自己的情緒和感受有什麼樣的理解?
Q7: 您目前採取哪些方式來應對自己負面情緒和感受?
Q8: 當您感到焦慮或壓力時, 您會如何處理?
Q9: 您身邊有哪些人可以支持您? 您會跟他們分享自己的困擾嗎?
Q10: 您是否願意嘗試新的方法來應對您目前面臨的狀況?

範例說明
** 避免二次傷害:
* 避免直接詢問個案關於爸爸的侵犯性行為細節，避免再次觸碰創傷。
* 使用更中性的詞彙描述個案的困擾，例如[不舒服的互動]代替[侵犯性行為]
* 將焦點放在個案的感受和理解上，例如[您對目前自己的情緒和感受有什麼樣的理解?]

** 整合三個議題
* Q1和Q2 針對[職場/校園適應]議題, 詢問個案對於工作的期望和自身狀況的影響
* Q3和Q4 針對[家庭關係]議題, 探討個案與父母的互動模式和感受
* Q5到Q10 針對[身心狀況]議題, 詢問個案對於自身情緒的理解和應對方式

** 避免重複
* 避免重複詢問個案已經填寫的資訊, 例如性別, 年齡, 職業等
* 使用更開放的問題, 讓個案自由表達, 例如[您有沒有想要補充分享的部分?]

** 注重個案感受
* 避免直接給予建議或評判,例如[您應該要]或「您不應該]
* 使用同理心和支持性的語言,例如[我理解您現在的感受] 或[您很棒，一直努力面對自己的困難]

** 提供選擇權
* 在Q10中，詢問個案是否願意嘗試新的方法,給予個案選擇的權利

** 注意事項
* 這只是一份範例問卷, 需要根據實際情況進行調整
* 在諮詢過程中, 心理師需要仔細觀察個案的反應, 並根據個案的狀況進行適當的調整
* 必要時, 心理師需要提供個案專業的幫助, 例如轉介其他資源"""


def execute_p0_post_effect(questions: list[QuestionType]):
    """ Inject static question into the generate questions """
    questions.append(QuestionType(type=QuestionTypeEnum.label,
                                  content="最後想邀請您做一個小小的問卷，請您仔細回想在最近一星期中(包括今天)，這些問題使您感到困擾或苦惱的程度，分別給予0-4分的分數，0分是完全沒有，4分是非常厲害"))

    questions.append(QuestionType(type=QuestionTypeEnum.number, content="感覺緊張不安"))
    questions.append(QuestionType(type=QuestionTypeEnum.number, content="感覺憂鬱"))
    questions.append(QuestionType(type=QuestionTypeEnum.number, content="情緒低落"))
    questions.append(QuestionType(type=QuestionTypeEnum.number, content="覺得比不上別人"))
    questions.append(QuestionType(type=QuestionTypeEnum.number, content="睡眠困難，譬如難以入睡、易醒或早醒"))
    questions.append(QuestionType(type=QuestionTypeEnum.number, content="有自殺的想法"))

    return questions


def execute_p1_post_effect(questions: list[QuestionType]):
    questions.append(QuestionType(type=QuestionTypeEnum.label,
                                  content="我理解有些話題可能會讓您感到不舒服或難以回答。如果您覺得不願意回應某些問題，您可以隨時跳過這些話題或暫時休息"))
    return questions


def execute_p2_post_effect(questions: list[QuestionType]):
    questions.append(QuestionType(type=QuestionTypeEnum.label,
                                  content="建議您可以從問卷中挑選至少5題您比較感興趣的話題回覆，幫助我們更了解您的狀況，為您訂製更貼合情況的治療策略"))
    return questions