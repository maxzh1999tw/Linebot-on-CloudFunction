# Linebot on Google Cloud Function
此範例展示了以 Cloud Fuction 事件驅動為核心的 LINE 對話機器人框架，
借鑑了 .NET 的 MVC 與 DI 概念，提升程式碼的可讀性與可擴展性。

## 部署方式
1. 啟用 GCP Cloud Function 與 FireStore API
2. 新增 Cloud Function 執行個體，並設定 Line Message API 環境變數 :
    - LINE_CHANNEL_SECRET
    - LINE_CHANNEL_ACCESS_TOKEN
3. 以 Python 3.9 部署程式碼，並將進入點設為 callback
4. 部署完成後到權限選單，將 allUsers 設為 Cloud Function 叫用者
5. 到觸發條件選單，即可取得 Webhook 網址
