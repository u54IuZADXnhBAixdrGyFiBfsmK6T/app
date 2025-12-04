render
    gunicorn app:app --workers 2 --bind 0.0.0.0:$PORT
    pip install -r requirements.txt
    GEMINI_API_KEY=""

# 1. PowerShell の実行権限
Set-ExecutionPolicy RemoteSigned -Scope CurrentUser -Force

# 2. pip アップデート
python -m pip install --upgrade pip

# 3. 仮想環境作成
python -m venv venv

# 4. 仮想環境アクティベート
.\venv\Scripts\Activate.ps1

# 5. ライブラリのインストール
pip install -r requirements.txt

# 6. APIキー設定
$env:GEMINI_API_KEY=""

# 7. アプリ起動
python app.py
