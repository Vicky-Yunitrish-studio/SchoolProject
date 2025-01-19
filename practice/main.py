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
        
        print("歡迎使用同理心對話系統！")
        print("1. 開始對話")
        print("2. 生成病人故事")
        print("3. 分析已有故事")
        print("4. 退出")
        
        while True:
            choice = input("\n請選擇功能 (1-4): ")
            
            if choice == "1":
                # 原有的對話功能
                while True:
                    user_input = input("\n請分享您的感受 (輸入 'back' 返回主選單)：")
                    if user_input.lower() == 'back':
                        break
                    response = empathy_llm.get_response(user_input)
                    print("\n助理回應：", response)
                    
            elif choice == "2":
                # 生成新故事
                print("\n正在生成病人故事...")
                story = empathy_llm.generate_patient_story()
                print("\n生成的故事：\n", story)
                
                # 詢問是否要分析故事
                if input("\n是否要分析這個故事？(y/n): ").lower() == 'y':
                    analysis = empathy_llm.analyze_patient_story(story)
                    print("\n故事分析：\n", analysis)
                    
            elif choice == "3":
                # 分析已有故事
                story = input("\n請輸入要分析的故事：\n")
                analysis = empathy_llm.analyze_patient_story(story)
                print("\n故事分析：\n", analysis)
                
            elif choice == "4":
                print("\n感謝使用！")
                break
                
    except Exception as e:
        print(f"系統初始化失敗：{str(e)}")
        print("請確保已安裝 Ollama 並執行 'ollama pull llama2' 下載模型")

if __name__ == "__main__":
    main()
