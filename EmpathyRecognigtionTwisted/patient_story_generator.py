from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
import json
import datetime

class PatientStoryGenerator:
    def __init__(self, llm):
        self.llm = llm
        self.story_template = self._create_story_template()
        self.story_chain = LLMChain(
            llm=self.llm,
            prompt=self.story_template
        )

    def _create_story_template(self):
        template = """請產生一個詳細的心理諮商個案背景故事，包含以下面向：

1. 基本資料：
- 年齡
- 性別
- 職業/學歷
- 家庭狀況

2. 主要困擾：
- 目前遇到的主要問題
- 症狀表現
- 困擾的持續時間

3. 壓力評估：
- 工作/學業壓力
- 人際關係壓力
- 家庭壓力
- 經濟壓力

4. 身心狀況：
- 睡眠品質
- 飲食狀況
- 情緒變化
- 生理症狀

5. 求助動機：
- 為何在此時尋求協助
- 期待得到的幫助

請用第三人稱敘述的方式，生成一個合理且具有連貫性的個案故事。

故事必須真實且具體，避免過於概括或模糊的描述。所有描述都應該要符合心理諮商的專業情境。

請開始生成：

"""
        return PromptTemplate(
            template=template,
            input_variables=[]
        )

    def generate_story(self):
        """生成一個新的病人故事"""
        try:
            story = self.story_chain.run()
            # 保存生成的故事
            self._save_story(story)
            return story
        except Exception as e:
            return f"生成故事時發生錯誤：{str(e)}"

    def _save_story(self, story, filename="patient_stories.json"):
        """保存生成的故事到 JSON 文件"""
        try:
            try:
                with open(filename, 'r', encoding='utf-8') as f:
                    stories = json.load(f)
            except FileNotFoundError:
                stories = {"stories": []}
            
            stories["stories"].append({
                "story": story,
                "timestamp": datetime.datetime.now().isoformat()
            })
            
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(stories, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"保存故事時發生錯誤：{str(e)}")

    def analyze_story(self, story):
        """分析故事中的關鍵信息"""
        analysis_template = """
        請分析以下個案故事，並提取關鍵信息：

        故事內容：
        {story}

        請提供以下分析：
        1. 主要問題類型
        2. 風險評估
        3. 建議的介入方向
        4. 需要特別注意的點
        """
        
        analysis_prompt = PromptTemplate(
            template=analysis_template,
            input_variables=["story"]
        )
        
        analysis_chain = LLMChain(
            llm=self.llm,
            prompt=analysis_prompt
        )
        
        return analysis_chain.run(story=story)
