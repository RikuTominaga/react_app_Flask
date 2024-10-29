from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware 

import sqlite3
import numpy as np
from sentence_transformers import SentenceTransformer
from langchain.embeddings import HuggingFaceEmbeddings
import faiss

# 1. SQLiteデータベースの準備
def create_faq_database():
    conn = sqlite3.connect("C:/react-info-app/backend/info.db") #データベースにアクセス（存在しない場合はデータベースを作成）
    cursor = conn.cursor() #データベースに命令するための変数
    cursor.execute("CREATE TABLE IF NOT EXISTS info (id INTEGER PRIMARY KEY, corporate_number TEXT, name TEXT , application_number TEXT, classifications TEXT, patent_type TEXT, title TEXT)") #もしもfaqという表がなければ作成する．
    
    conn.commit() #実行が反映

    return conn #データベースのオブジェクト変数を戻り値とする．あとでこのデータベースからデータを取り出すため．

# 2. 文章の埋め込みの作成
def compute_faq_embeddings(faq_questions, model):
    return np.array(model.embed_documents(faq_questions)) #model.encodeで文字列をベクトル化する

# 3. Faissインデックスの作成　Faissとはベクトル専用のデータベース
def create_faiss_index(model, embeddings, doc_ids):
    dimension=768
    index_flat = faiss.IndexFlatIP(dimension) #指定次元のベクトルを格納するFaissを整備.ベクトルの距離（コサイン）を計算できるよう初期化
    index = faiss.IndexIDMap(index_flat) #IDをベクトルに付与する（マッピング）
    index.add_with_ids(embeddings, doc_ids) #実際に文書のベクトルにIDを振ってデータベースに格納
    return index, index_flat

# 4. クエリ処理
def search_faq(query, model, index, k=3):
    query_embedding = model.embed_query(query) #質問文をベクトル化
    distances, indices = index.search(np.array([query_embedding],dtype=np.float32), k) #Faissデータベースから類似している文のトップ3を取得．kはトップkまで取得する意味
    return distances[0],indices[0]

# 5. 結果の取得
def get_faq_results(faq_ids, conn):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM info WHERE id IN ({})".format(",".join("?" * len(faq_ids))), faq_ids) #結果をデータベースから取得
    return cursor.fetchall()

# データベース作成
conn = create_faq_database() #connはデータベースのオブジェクト変数
com_list=[]

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post('/api/query')
async def index(request: Request):
        data = await request.json()
        query = data.get('query')
        
        #create_faq_database()
        conn = sqlite3.connect("C:/react-info-app/backend/info.db") #データベースにアクセス（存在しない場合はデータベースを作成）
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM info") #faqから文をすべて取得する
        faq_data = cursor.fetchall() #結果をリストに格納

        print(faq_data)

        global com_list
        com_list=[]

        faq_ids, corporate_number, name,application_number,classifications,patent_type, faq_questions = zip(*faq_data) #リストをIDとテキストに分ける
        model=HuggingFaceEmbeddings(model_name="intfloat/multilingual-e5-base")

        embeddings=compute_faq_embeddings(faq_questions, model)
        index, index_flat = create_faiss_index(model, embeddings, faq_ids)

        faq_distances,faq_indices = search_faq(query, model, index_flat,k=7) #質問文と類似している文を獲得

        # 結果を取得して表示
        results = get_faq_results([faq_ids[i] for i in faq_indices], conn)
        print("Results for query:", query)
        for r,d in zip(results,faq_distances):
            print(f"ID: {r[0]}, Corporate_number: {r[1]},name: {r[2]} , title: {r[6]}, Simularity:{d}, {r[4][37:-3]}")
            com_list.append([r[1],r[2],r[3],r[5],r[4][37:-3],r[6],float(d) if isinstance(d, np.float32) else d])

        # データベース接続を閉じる
        conn.close()

        return com_list
