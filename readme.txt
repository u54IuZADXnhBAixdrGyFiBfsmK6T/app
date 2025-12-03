gunicorn app:app --workers 2 --bind 0.0.0.0:$PORT
pip install -r requirements.txt

pipアップグレード
python -m pip install --upgrade pip

$env:GEMINI_API_KEY=""


スクリプト実行許可
Set-ExecutionPolicy RemoteSigned -Scope CurrentUser -Force

仮想環境を作成
python -m venv venv


仮想環境をアクティベート
.\venv\Scripts\Activate.ps1


 必要な全ライブラリをインストール
pip install -r requirements.txt


APIキーを設定
$env:GEMINI_API_KEY=""


起動
python app.py