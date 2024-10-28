# similar item searcher  

## 開発環境・ライブラリー情報
- Windows 11
- Python 3.9.7
- react 18.3.1
- axios 1.7.7
- sentence-transformers 3.2.0
- langchain-community 0.3.2
- faiss-cpu 1.9.0
### Flaskを使用する場合
- Flask 3.0.3
- Flask-Cors 5.0.0
### FastAPIを使用する場合
- fastapi 0.115.4

## 構築手順
1. プロジェクト作成  
`npx create-react-app react-info-app`
2. backendフォルダーをreact-info-appに新規作成
3. 添付のapp.pyもしくはmain.pyとinfo.dbをbackend配置
4. App.jsとApp.cssを添付のApp.jsとApp.cssに書換
5. 仮想環境の作成  
`python -m venv venv`  
6. 仮想環境のアクティベート  
`.\venv\Scripts\activate`
## ディレクトリ構成
```
7. ライブラリーのインストール
.  
└── react-info-app/  
    ├── .venv/  
    │   └── ...  
    ├── node_modules/  
    │   └── ...  
    ├── bakend/ #新規作成  
    │   ├── venv   
    │   ├── app.py or main.py #添付のapp.pyもしくはmain.py配置  
    │   └── info.db #添付のinfo.dbを配置  
    ├── public/    
    │   └── ...  
    ├── src/
    │   ├── App.css #書換  
    │   ├── App.js #書換  
    │   ├── App.test.js  
    │   ├── index.css  
    │   ├── index.js  
    │   └── ...  
    ├── .gitignore  
    ├── package-lock.json  
    ├── package.json  
    └── READNE.md
```
