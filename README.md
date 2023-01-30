## 概要
[各府省の新着](https://www.kantei.go.jp/jp/joho/news/index.html)の差分をLINE通知する。各府省のRSSを個別購読するのが面倒なので作成。

## 仕様
- scrapyを使用
- 1ページ目をスクレイピングして新着情報を取得
- 差分があれば日付ごとにファイル出力とLINE通知する
- ファイル保持期間は1週間
- 1ページ目しか見ないので定期実行間隔の間に2ページ以上更新があった場合は検知されない
- LINE Notify TOKENをsecretsで管理