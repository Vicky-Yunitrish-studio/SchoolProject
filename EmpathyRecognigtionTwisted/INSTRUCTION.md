# 同理心對話與認知扭曲辨識系統建置指南

本指南將幫助您建立一個基於 LLaMA 模型的同理心對話系統，包含資料生成、模型整合和對話互動功能。

## 1. 環境準備

### 1.1 建立專案結構
```bash
mkdir -p EmpathyRecognigtionTwisted/data
cd EmpathyRecognigtionTwisted
```

### 1.2 安裝依賴套件
建立 requirements.txt 並安裝依賴：
```bash
pip install -r requirements.txt
```

### 1.3 安裝 Ollama
1. 前往 [Ollama 官網](https://ollama.ai/) 下載並安裝
2. 執行以下命令下載模型：
```bash
ollama pull llama3.3
```

## 2. 專案檔案結構
```
EmpathyRecognigtionTwisted/
├── __init__.py
├── main.py
├── llm_integration.py
├── patient_story_generator.py
├── generate_empathy_data.py
├── requirements.txt
└── data/
    ├── empathy_cognitive_dataset.json
    └── patient_stories.json
```

## 3. 實作步驟

### 3.1 建立資料生成模組
1. 創建 `generate_empathy_data.py`
- 實現同理心對話模板
- 定義問題類型和認知扭曲模板
- 建立資料生成和儲存功能

### 3.2 實現病人故事生成器
1. 創建 `patient_story_generator.py`
- 定義故事生成模板
- 實現故事分析功能
- 建立資料保存機制

### 3.3 整合 LLM 功能
1. 創建 `llm_integration.py`
- 設置 Ollama 模型
- 實現向量數據庫
- 建立對話鏈和記憶功能

### 3.4 建立主程式
1. 創建 `main.py`
- 整合所有功能模組
- 實現互動介面

## 4. 運行程式

```bash
python main.py
```

## 5. 功能說明

### 5.1 資料生成
- 自動生成同理心對話資料集
- 生成認知扭曲對話範例
- 儲存於 JSON 格式檔案

### 5.2 模型功能
- 使用 LLaMA 模型進行對話生成
- RAG (檢索增強生成) 功能
- 對話歷史記憶功能

### 5.3 互動功能
- 同理心對話互動
- 病人故事生成
- 故事分析功能

## 6. 進階配置

### 6.1 模型參數調整
可在 `llm_integration.py` 中調整：
- 模型溫度 (temperature)
- 檢索數量 (k 值)
- 提示詞模板

### 6.2 資料模板擴充
可在 `generate_empathy_data.py` 中增加：
- 新的問題類型
- 情緒表達方式
- 回應模板

## 7. 故障排除

### 常見問題
1. 模型載入失敗
```bash
ollama pull llama3.3
```

2. 依賴套件問題
```bash
pip install -r requirements.txt --upgrade
```

3. 資料目錄問題
```bash
mkdir -p data
```

## 8. 後續開發建議

1. 新增功能
- 語音互動整合
- 多語言支援
- Web 介面

2. 改進方向
- 擴充資料集
- 優化提示詞
- 增加評估指標

## 9. 注意事項

- 確保 Ollama 服務正常運行
- 檢查資料目錄權限
- 定期備份生成的資料
