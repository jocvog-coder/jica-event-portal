# JICA イベント情報ポータル - GitHub Pages デプロイガイド

## 📚 このガイドについて

このドキュメントは、JICA海外協力隊イベント情報ポータルを GitHub Pages 上で公開し、
自動的にイベント情報を更新する仕組みを構築するための完全なガイドです。

## ✅ 準備するもの

- GitHub アカウント
- インターネット接続
- テキストエディタ

## 🚀 デプロイ手順（全10ステップ）

### ステップ1: GitHub でリポジトリを作成

1. GitHub にログイン（https://github.com）
2. 右上の `+` をクリック → `New repository`
3. リポジトリ名: `jica-event-portal`（任意）
4. 説明: `JICA海外協力隊 イベント情報ポータル`
5. **Public** を選択（重要）
6. `Create repository` をクリック

### ステップ2: ローカルでリポジトリを初期化

```bash
# ターミナルで実行
mkdir jica-event-portal
cd jica-event-portal

git init
git branch -M main
git config user.name "Your Name"
git config user.email "your.email@example.com"
```

### ステップ3: ファイルをコピー

提供されているファイルをプロジェクトフォルダにコピーします：

```
jica-event-portal/
├── index.html                # メインページ
├── events.json              # イベント情報（自動更新）
├── scrape_jica_events.py    # スクレイピングスクリプト
├── requirements.txt         # Python 依存関係
├── README.md               # プロジェクト説明
└── .github/workflows/
    └── scrape-events.yml   # GitHub Actions 設定
```

`.github/workflows/` フォルダが無い場合は手動で作成してください。

### ステップ4: ファイルを git に追加

```bash
git add .
git commit -m "Initial commit: JICA Event Portal"
```

### ステップ5: GitHub にプッシュ

```bash
git remote add origin https://github.com/your-username/jica-event-portal.git
git push -u origin main
```

（`your-username` は自分の GitHub ユーザー名に置き換えてください）

### ステップ6: GitHub Pages を有効化

1. リポジトリのページで `Settings` をクリック
2. 左メニューから `Pages` を選択
3. "Source" で `Deploy from a branch` を選択
4. Branch を `main` に、フォルダを `/ (root)` に設定
5. `Save` をクリック

### ステップ7: GitHub Actions の権限を設定

1. `Settings` → `Actions` → `General`
2. "Workflow permissions" セクションまでスクロール
3. `Read and write permissions` を選択
4. `Save` をクリック

### ステップ8: 初回手動実行

1. リポジトリのページで `Actions` タブをクリック
2. 左メニューから `JICA Events Auto-Scrape` を選択
3. `Run workflow` をクリック
4. `Run workflow` を確認

### ステップ9: 確認

1. 数分待つ（最大5分）
2. `Actions` タブで実行が完了したか確認（緑チェック）
3. リポジトリに `events.json` が更新されたか確認

### ステップ10: サイトへアクセス

サイトが以下のURLで公開されます：

```
https://your-username.github.io/jica-event-portal/
```

（`your-username` は自分の GitHub ユーザー名）

## 🔄 自動更新の仕組み

GitHub Actions により、以下のスケジュールで自動実行されます：

- **実行タイミング**: 毎日 UTC 00:00 (日本時間 09:00)
- **実行内容**: 
  1. `scrape_jica_events.py` を実行
  2. 複数ソースからイベント情報を取得
  3. `events.json` を更新
  4. 自動で Git に commit & push

## 📝 使い方

### イベント一覧を表示

サイトにアクセスすると、自動集約されたイベント情報が表示されます：

- **カレンダー表示**: 月間カレンダーでイベントを確認
- **カテゴリフィルター**: ネットワーキング、同窓会などで絞り込み
- **イベント詳細**: 各イベントをクリックで詳細表示

### 手動でイベント情報を更新

GitHub Actions の実行を待たずに即座に更新したい場合：

1. `Actions` タブをクリック
2. `JICA Events Auto-Scrape` ワークフローを選択
3. `Run workflow` をクリック

## 🔧 カスタマイズ

### 新しいイベントソースを追加

`scrape_jica_events.py` にメソッドを追加します：

```python
def scrape_my_custom_source(self):
    """カスタムソースからイベント情報を取得"""
    # ここにスクレイピングコードを記述
    self.add_event(
        title="イベント名",
        date="2026-04-10",
        time="18:30～20:30",
        location="東京都",
        description="説明",
        category="networking",
        source_url="https://example.com",
        source_name="ソース名"
    )

# scrape_all() メソッドに追加
def scrape_all(self):
    self.scrape_jica_official()
    self.scrape_joca_events()
    self.scrape_rss_feeds()
    self.scrape_my_custom_source()  # ← 追加
    self.scrape_regional_networks()
```

### 表示デザインを変更

`index.html` を任意のテキストエディタで開いて、CSS部分を修正します。

### カテゴリを追加

1. `scrape_jica_events.py` の `add_event()` で新しいカテゴリを指定
2. `index.html` の CSS に新しい色定義を追加
3. `getCategoryLabel()` 関数に新しいラベルを追加

## 🐛 トラブルシューティング

### サイトが表示されない

- **確認項目**:
  1. GitHub Pages が `Settings` で有効になっているか
  2. ブランチが `main` になっているか
  3. URL が正しいか (`https://username.github.io/repo-name/`)
  4. 大文字小文字が正しいか

### イベント情報が表示されない

- **確認項目**:
  1. `events.json` がリポジトリに存在するか
  2. JSON 形式が正しいか
  3. ブラウザのキャッシュをクリアしたか（Ctrl+Shift+Delete）
  4. Developer Console にエラーがないか（F12）

### GitHub Actions がエラーになった

1. `Actions` タブで失敗したワークフローをクリック
2. ジョブのログを確認
3. 一般的なエラー：
   - **ImportError**: `requirements.txt` を確認
   - **ConnectionError**: Webサイトの構造変更
   - **Permissions**: `Settings` → `Actions` → `Permissions` を確認

## 📊 サイト構成

```
index.html
├── ヘッダー
├── フィルターコントロール
├── カレンダー表示
│   └── events.json からイベント読み込み
└── イベント一覧
    └── カテゴリ別に表示
```

## 🔐 セキュリティに関する注意

- **リポジトリを Public にしても大丈夫**
  - スクレイピングスクリプトとイベント情報のみ
  - 個人情報や機密情報は含まれていない

- **API キーがある場合**
  - `Settings` → `Secrets and variables` → `Actions` に保存
  - 環境変数として呼び出し

## 📱 モバイル対応

ポータルサイトはレスポンシブデザインに対応しており、
スマートフォン、タブレット、デスクトップで最適に表示されます。

## 🌐 独自ドメインの設定（オプション）

GitHub Pages は独自ドメインをサポートしています：

1. DNS 設定でドメインを指定
2. `Settings` → `Pages` → `Custom domain` に入力
3. HTTPS を有効化

## 📞 サポート

問題が発生した場合：

1. このドキュメントを読み直す
2. GitHub Issues で検索
3. GitHub Discussion で質問

## 🎉 次のステップ

- [ ] サイトにアクセスして動作確認
- [ ] イベントソースを追加カスタマイズ
- [ ] 友人・同僚に共有
- [ ] フィードバックを収集して改善

---

**作成日**: 2026年3月19日  
**最終更新**: 2026年3月19日
