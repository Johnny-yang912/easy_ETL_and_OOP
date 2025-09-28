# easy_ETL_and_OOP

## 💡 專案動機
這個專案是為了補足求職所需的技能而設計的。
許多工作內容強調 ETL 經驗、Airflow 操作經驗，以及自寫 OOP 模組的能力。過去我雖然在學習過程中接觸過 OOP，但規模較大的程式多半是依賴 AI 輔助完成，因此我希望能自己實作一個小型專案，從零開始掌握這些基礎。
本專案展示了 ETL 與 Airflow 的最基本流程：本地下載資料 → 進行轉換 → 輸入 SQLite。
在資料轉換部分，我以 OOP 方式設計了一個簡單的 Transformer，負責處理單一時間欄位，將日期切分並新增「小時」欄位，藉此驗證自訂物件導向模組在 Pipeline 中的可行性。

---

## 📂 專案結構

```
easy_ETL_and_OOP/
│── dags/                 # Airflow DAGs (ETL 工作流)
│   └── etl_pipeline.py
│── data/                 # 範例資料 (input.csv 保留)
│   └── input.csv
│── db/                   # SQLite 資料庫 (自動生成，已忽略)
│── logs/                 # Airflow log (自動生成，已忽略)
│── plugins/              # Airflow plugins
│── src/                  # 自訂模組
│   └── transformers/     # 自訂 Transformer
│── test/                 # 測試程式
│── docker-compose.yml    # 建立 Airflow 環境
│── requirements.txt      # Python 依賴套件
│── .env                  # 環境變數設定 (已忽略)
```

---

## 🚀 功能簡介
- Extract: 從 data/input.csv 讀取資料
- Transform: 透過 src/transformers/ 內的自訂模組清理與轉換
- Load: 輸出到 SQLite (pipeline_etl.db)
- Airflow 整合: 使用 etl_pipeline.py 建立 DAG，目前以 手動觸發 方式執行 ETL 任務；同時也預留結構，可輕鬆擴展為自動排程版本

---

## 🔧 環境安裝
1. 啟動 Docker 與 Docker Compose
2. 建立並啟動 Airflow 環境：
```
docker-compose up -d
```
3.開啟瀏覽器 → http://localhost:18080

---

## 📊 使用方式
1. 把新的原始資料放到 data/
2. 透過 Airflow DAG (etl_pipeline) 手動觸發 執行 ETL 流程（結構上可輕鬆擴展為自動排程版本）
3. 結果會存到 db/pipeline_etl.db

---

## 📌 未來改進
- 增加更多 Transformer
- 加入資料驗證與錯誤處理
- 嘗試接入其他資料來源（API / DB）
