import os
from EmpathyRecognigtionTwisted.generate_empathy_data import generate_dialogue, save_dataset
from llm_integration import EmpathyLLM

def main():
    # 確保資料集存在
    if not os.path.exists("empathy_cognitive_dataset.json"):
        conversations = generate_dialogue()
        save_dataset(conversations)
    
    # 初始化 LLM 系統，使用 llama2 模型
    try:
        empathy_llm = EmpathyLLM(model_name="llama2")
        
        print("歡迎使用同理心對話系統！（輸入 'quit' 結束對話）")
        
        while True:
            user_input = input("\n請分享您的感受：")
            if user_input.lower() == 'quit':
                break
                
            try:
                response = empathy_llm.get_response(user_input)
                print("\n助理回應：", response)
            except Exception as e:
                print(f"發生錯誤：{str(e)}")
                break
        
        print("\n感謝使用！")
    except Exception as e:
        print(f"系統初始化失敗：{str(e)}")
        print("請確保已安裝 Ollama 並執行 'ollama pull llama2' 下載模型")

if __name__ == "__main__":
    main()
