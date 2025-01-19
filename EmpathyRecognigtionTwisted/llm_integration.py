from langchain.llms import Ollama
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import Chroma
from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationBufferMemory
from langchain.prompts import PromptTemplate
from patient_story_generator import PatientStoryGenerator
import os
import json
import random
from typing import Dict, Any

class EmpathyLLM:
    def __init__(self, model_name="llama3.3", dataset_path=None):
        if dataset_path is None:
            dataset_path = os.path.join(os.path.dirname(__file__), "data", "empathy_cognitive_dataset.json")
        # 使用 Ollama 本地模型
        self.llm = Ollama(
            model=model_name,
            temperature=0.7
        )
        
        # 使用 HuggingFace 的 sentence-transformers 作為 embeddings
        self.embeddings = HuggingFaceEmbeddings(
            model_name="sentence-transformers/all-MiniLM-L6-v2"
        )
        
        self.dataset_path = dataset_path
        self.memory = ConversationBufferMemory(
            memory_key="chat_history",
            return_messages=True
        )
        
        # 初始化向量數據庫
        self.vector_store = self._initialize_vector_store()
        
        # 設置對話鏈
        self.chain = self._setup_conversation_chain()

    def _initialize_vector_store(self):
        # 讀取訓練數據
        with open(self.dataset_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # 準備文檔
        texts = [
            f"Instruction: {conv['instruction']}\nInput: {conv['input']}\nOutput: {conv['output']}"
            for conv in data['conversations']
        ]
        
        # 創建向量數據庫
        return Chroma.from_texts(
            texts,
            self.embeddings,
            collection_name="empathy_cognitive"
        )

    def _setup_conversation_chain(self):
        patient_info = self._setup_patient_chain()
        
        prompt_template = """
        你是一個具有高度同理心的助理，專門幫助人們處理情緒和認知問題。請使用繁體中文回應。
        
        個案資訊：
        - 情緒狀態: {patient_info[emotional_state]}
        - 壓力指數: {patient_info[stress_level]}/10
        - 健康狀況: {", ".join(patient_info[health_condition])}
        - 人際關係: {patient_info[relationship_status]}
        
        相關參考資訊：
        {context}
        
        歷史對話：
        {chat_history}
        
        當前問題：
        {question}
        
        請用同理心和專業的方式回應：
        """
        
        PROMPT = PromptTemplate(
            input_variables=["context", "chat_history", "question", "patient_info"],
            template=prompt_template
        )
        
        return ConversationalRetrievalChain.from_llm(
            llm=self.llm,
            retriever=self.vector_store.as_retriever(
                search_kwargs={"k": 3}
            ),
            memory=self.memory,
            combine_docs_chain_kwargs={
                "prompt": PROMPT,
                "patient_info": patient_info
            },
            return_source_documents=True
        )

    def _setup_patient_chain(self) -> Dict[str, Any]:
        emotions = ['焦慮', '沮喪', '憤怒', '害怕', '煩躁']
        relationships = ['家庭關係緊張', '工作人際困擾', '感情問題', '社交障礙']
        health_issues = ['失眠', '頭痛', '食慾不振', '注意力難以集中']
        
        patient_info = {
            "emotional_state": random.choice(emotions),
            "relationship_status": random.choice(relationships),
            "health_condition": random.sample(health_issues, 2),
            "stress_level": random.randint(1, 10),
            "support_system": random.choice(['較強', '普通', '較弱']),
            "coping_mechanisms": random.sample(['運動', '冥想', '寫日記', '聽音樂'], 2)
        }
        
        return patient_info

    def get_response(self, user_input):
        """獲取 LLM 的回應"""
        try:
            response = self.chain({"question": user_input})
            return response['answer']
        except Exception as e:
            return f"抱歉，處理您的請求時發生錯誤：{str(e)}"

    def reset_conversation(self):
        """重置對話歷史"""
        self.memory.clear()
