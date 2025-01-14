import json
import random

# 同理心對話模板
empathy_templates = [
    {
        "situation": "一個人正在經歷{problem}",
        "feeling": [
            "難過", "沮喪", "焦慮", "生氣", "害怕", "孤單", "無助", 
            "疲憊", "壓力大", "不安", "挫折", "失望"
        ],
        "empathy_response": [
            "我理解你現在感到{feeling}，這確實是一個困難的處境。",
            "聽到你遇到{problem}，我能感受到你的{feeling}。",
            "面對{problem}時感到{feeling}是很自然的事。",
            "你現在感到{feeling}是可以理解的，{problem}確實不容易處理。",
            "這樣的{problem}的確會讓人感到{feeling}，你的感受是合理的。",
            "聽起來{problem}帶給你很大的壓力，讓你感到{feeling}。",
            "這樣的{feeling}感受我完全能夠理解，面對{problem}確實需要很大的勇氣。"
        ]
    }
]

def generate_dialogue():
    conversations = []
    
    # 擴充問題類型
    problems = {
        "工作壓力": [
            "工作量過大", "面臨裁員", "與主管意見不合", 
            "工作績效壓力", "職場人際關係", "工作倦怠",
            "新工作適應", "職涯轉換"
        ],
        "人際關係困擾": [
            "與家人衝突", "朋友疏遠", "感情問題", 
            "社交焦慮", "人際疏離", "溝通障礙",
            "被誤解", "信任議題"
        ],
        "學業挑戰": [
            "考試壓力", "作業負擔", "學習困難", 
            "時間管理", "成績壓力", "專業選擇",
            "論文瓶頸", "課業跟不上"
        ],
        "健康問題": [
            "身體不適", "慢性病", "睡眠問題", 
            "精神壓力", "飲食失調", "運動傷害",
            "過度疲勞", "焦慮症狀"
        ],
        "生活壓力": [
            "經濟困難", "居住問題", "生活規劃", 
            "時間壓力", "環境適應", "未來焦慮",
            "家庭負擔", "生活轉變"
        ]
    }

    # 認知扭曲模板
    cognitive_distortion_templates = [
        {
            "distortion_type": "非黑即白思考",
            "thought_pattern": [
                "如果我沒有做到完美，就是完全失敗。",
                "要嘛全部做對，要嘛就是一無是處。",
                "這件事不是成功就是失敗，沒有中間地帶。",
                "如果不能做到最好，那就不要做了。"
            ],
            "rational_response": [
                "事情並非非黑即白，存在很多中間狀態。",
                "部分成功也是進步的開始。",
                "人生充滿各種可能性，不是只有成功和失敗兩種結果。",
                "每個過程都有其價值，完美並不是唯一的標準。"
            ]
        },
        {
            "distortion_type": "過度概化",
            "thought_pattern": [
                "我總是搞砸每件事。",
                "沒有人會喜歡我。",
                "事情永遠不會變好。",
                "我永遠做不好這件事。"
            ],
            "rational_response": [
                "試著具體回想，是否真的每次都是這樣？",
                "這可能是一時的挫折，而不是永恆的真理。",
                "每個人都有擅長和不擅長的事情。",
                "改變是漸進的，給自己時間和空間成長。"
            ]
        },
        {
            "distortion_type": "心理過濾",
            "thought_pattern": [
                "雖然大家說報告很好，但有一個小缺陷就代表整個都失敗了。",
                "雖然今天做了很多事，但沒完成一件就代表整天都浪費了。",
                "只要有一個人不喜歡我，就表示我很失敗。"
            ],
            "rational_response": [
                "試著平衡地看待成功和需要改進的地方。",
                "肯定已經完成的部分，同時思考如何改進。",
                "沒有人可以讓所有人都滿意，這是很正常的。"
            ]
        }
    ]

        # 修改生成對話的部分
    for category, specific_problems in problems.items():
        for _ in range(10):  # 每個類別生成10個對話
            template = random.choice(empathy_templates)
            problem = random.choice(specific_problems)
            feeling = random.choice(template["feeling"])
            response = random.choice(template["empathy_response"]).format(
                problem=problem,
                feeling=feeling
            )
            
            conversations.append({
                "instruction": f"對方正在經歷{problem}，表現出同理心",
                "input": f"我最近因為{problem}感到很{feeling}...",
                "output": response
            })
    
    # 生成認知扭曲對話
    for template in cognitive_distortion_templates:
        for thought in template["thought_pattern"]:
            response = random.choice(template["rational_response"])
            conversations.append({
                "instruction": f"辨識並回應{template['distortion_type']}的認知扭曲",
                "input": thought,
                "output": response
            })
    
    return conversations

def save_dataset(conversations, filename="empathy_cognitive_dataset.json"):
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump({"conversations": conversations}, f, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    conversations = generate_dialogue()
    save_dataset(conversations)
    print(f"已生成 {len(conversations)} 筆對話資料")
