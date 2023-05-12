# github_app について

issue または pullrequest に自動でコメントする

## 動作

1. ターミナルで`cd ~/github_app`に移動して
2. `smee -u https://smee.io/9PrVoBhWAqLuBF1p --port 5000`を実行
3. app.py を run 指せる（左上の三角マーク ▶）
4. issue / pullrequest を作成

## エラーについて

- `openai.error.AuthenticationError: <empty message>:`
  apikey の期限が切れているとき -> 更新が必要
- `openai has no Attribute Completion`
  ファイル名と変数名が競合している -> ファイル名を変更
