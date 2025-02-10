#!/bin/bash

# Python仮想環境の作成
python -m venv venv

# 仮想環境のアクティベート
source venv/bin/activate

# 必要なパッケージのインストール
pip install -r requirements.txt

echo "セットアップが完了しました。"
echo "スクリプトを実行するには以下のコマンドを実行してください："
echo "source venv/bin/activate"
echo "python main.py"
