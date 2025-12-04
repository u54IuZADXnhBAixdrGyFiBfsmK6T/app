# app.py
import os
from flask import Flask, render_template, request, jsonify
from google import genai
from google.genai import types

app = Flask(__name__)


# 1. Gemini APIクライアントの初期化
# 環境変数 GEMINI_API_KEY からAPIキーを読み込む
try:
    client = genai.Client()
except Exception as e:
    print(f"Gemini APIクライアントの初期化中にエラーが発生しました: {e}")
    # APIキーが設定されていない場合はエラーを出しつつ、アプリ自体は起動させる
    client = None

#2. Webページの表示（HTMLファイルの読み込み）

@app.route('/')
def index():
    return render_template('index.html')

# 3. Geminiにリクエストを送信するAPIエンドポイント
@app.route('/get_recommendation', methods=['POST'])
def get_recommendation():
    if client is None:
        return jsonify({"error": "Gemini APIキーが設定されていません。ターミナルを確認してください。"}), 500
        
    # フロントエンドから送られてきたユーザーデータを取得
    data = request.json
    height = data.get('height')
    weight = data.get('weight')
    activity = data.get('activity')
    ideal = data.get('ideal')

    # ユーザーの情報をプロンプトに組み込む
    prompt = f"""
    あなたはプロの栄養士とフィットネストレーナーです。
    以下のユーザー情報に基づいて、**最適な食事の提案（3食分）**と、**簡単なトレーニングメニュー（3種類）**を提案してください。
    出力は前説はいりません。いきなり本題から入ってください

    【制約事項】
    - 出力は**Markdown形式**で記述してください。
    - 重要なキーワードは太字(**)を使って強調してください。
    - 見出しは ## を使用してください。
    - リストは見やすいように箇条書きを使用してください。

    文字数は少な目でよいです

    【ユーザー情報】
    - 身長 : {height} cm
    - 体重 : {weight} kg
    - 日常生活の過ごし方 : {activity}
    - 理想の体型 :{ideal}
    
    【提案の形式】
    提案はMarkdown形式で、必ず以下の2つのセクション見出しを含めてください。
    
    ## 🍽️ おすすめの献立
    （提案理由と、朝食・***昼食***・***夕食***の具体的なメニューを記述。**「昼食」と「夕食」という文字自体をMarkdownの太字（`**`）で囲んでください**。）
    ## 💪 トレーニングメニュー
    （提案理由と、トレーニング名、回数/時間を記述）
    """
    
    try:
        # Gemini APIを呼び出す
        response = client.models.generate_content(
            model='gemini-2.5-flash', # 高速でコスト効率の良いモデルを選択
            contents=prompt
        )
        
        # Geminiからの回答（テキスト）をそのままJSONで返す
        return jsonify({"recommendation": response.text})

    except Exception as e:
        # API呼び出しでエラーが発生した場合の処理
        return jsonify({"error": f"Gemini APIの呼び出し中にエラーが発生しました: {e}"}), 500

if __name__ == '__main__':
    app.run(debug=True)