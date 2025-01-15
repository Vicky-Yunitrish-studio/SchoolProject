from langchain.llms import Ollama
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import Chroma
from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationBufferMemory
from langchain.prompts import PromptTemplate
import json

class EmpathyLLM:
    def __init__(self, model_name="llama2", dataset_path="empathy_cognitive_dataset.json"):
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
        prompt_template = """
        你是一個具有高度同理心的助理，專門幫助人們處理情緒和認知問題。請使用繁體中文回應。
        
        相關參考資訊：
        {context}
        
        歷史對話：
        {chat_history}
        
        當前問題：
        {question}
        
        請用同理心和專業的方式回應：
        """
        
        PROMPT = PromptTemplate(
            input_variables=["context", "chat_history", "question"],
            template=prompt_template
        )
        
        return ConversationalRetrievalChain.from_llm(
            llm=self.llm,
            retriever=self.vector_store.as_retriever(
                search_kwargs={"k": 3}
            ),
            memory=self.memory,
            combine_docs_chain_kwargs={"prompt": PROMPT},
            return_source_documents=True
        )

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
