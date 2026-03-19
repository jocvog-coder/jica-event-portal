# JICA海外協力隊 イベント情報ポータル

複数のソースからJICA海外協力隊関連のイベント情報を自動集約し、カレンダー形式で表示するポータルサイトです。

## 📋 プロジェクト概要

このプロジェクトは以下の特徴を持ちます：

- **自動集約**: 複数のソースから定期的にイベント情報を自動取得
- **完全無料**: GitHub Pages でホスティング、GitHub Actions で自動更新
- **カレンダー表示**: 月間カレンダーでイベントを一目で確認
- **カテゴリフィルター**: ネットワーキング、同窓会などで絞り込み
- **レスポンシブデザイン**: スマートフォンにも対応

## 🏗️ システム構成

```
JICA-Event-Portal/
├── index.html              # メインのポータルサイト
├── scrape_jica_events.py   # イベント情報自動取得スクリプト
├── events.json             # 取得したイベント情報（JSON形式）
├── .github/
│   └── workflows/
│       └── scrape-events.yml  # GitHub Actions ワークフロー
└── README.md              # このファイル
```

## 📊 データ取得元

現在のバージョンでは以下のソースからイベント情報を取得します：

1. **JICA公式サイト** (https://www.jica.go.jp/)
2. **JOCA** (日本海外協力隊協会) (https://www.joca.or.jp/)
3. **RSS フィード** (各種JICA関連ニュース)
4. **地域別OB・OG会** (Facebook、各支部ホームページ)

## 🚀 セットアップ方法

### 前提条件

- GitHub アカウント
- Python 3.7 以上（ローカルテスト用）

### ステップ1: リポジトリの作成

1. GitHub で新しいリポジトリを作成します
   - リポジトリ名: `jica-event-portal` (または任意の名前)
   - 説明: "JICA海外協力隊 イベント情報ポータル"

2. ローカルにクローンします
```bash
git clone https://github.com/your-username/jica-event-portal.git
cd jica-event-portal
```

### ステップ2: ファイルの配置

以下のファイルをリポジトリに配置します：

```bash
# メインのHTMLファイル
cp index.html ./

# Pythonスクリプト
cp scrape_jica_events.py ./

# GitHub Actions ワークフロー
mkdir -p .github/workflows
cp scrape-events.yml .github/workflows/
```

### ステップ3: GitHub Actions の設定

1. リポジトリの Settings → Actions → General へ
2. "Workflow permissions" を確認
3. "Read and write permissions" に設定

### ステップ4: 初回実行

```bash
# ローカルで動作確認
pip install requests beautifulsoup4 feedparser
python scrape_jica_events.py

# events.json が生成されることを確認
```

### ステップ5: GitHub Pages の有効化

1. リポジトリの Settings → Pages へ
2. "Source" を "main branch" に設定
3. サイトが `https://your-username.github.io/jica-event-portal/` で公開されます

## 📅 自動更新スケジュール

GitHub Actions により、毎日 UTC 00:00 (日本時間 09:00) に自動でイベント情報が更新されます。

手動で実行したい場合：
1. GitHub の Actions タブへ
2. "JICA Events Auto-Scrape" を選択
3. "Run workflow" をクリック

## 🔧 スクリプトのカスタマイズ

### イベント取得元の追加

`scrape_jica_events.py` の `JICAEventScraper` クラスに新しいメソッドを追加：

```python
def scrape_custom_source(self):
    """カスタムソースからイベント情報を取得"""
    # スクレイピング処理
    self.add_event(
        title="イベント名",
        date="2026-04-10",
        time="18:30～20:30",
        location="東京都",
        description="説明",
        category="networking",
        source_url="https://...",
        source_name="ソース名"
    )
```

その後、`scrape_all()` メソッドで新しいメソッドを呼び出します：

```python
def scrape_all(self):
    self.scrape_jica_official()
    self.scrape_joca_events()
    self.scrape_rss_feeds()
    self.scrape_custom_source()  # 追加
    self.scrape_regional_networks()
```

### カテゴリの追加

イベントカテゴリを増やす場合は、以下の場所を修正：

1. `scrape_jica_events.py` の `add_event()` 呼び出し
2. `index.html` の CSS (`.badge-` と `.event-category.`)
3. `index.html` の `getCategoryLabel()` 関数

## 📝 JSON データ形式

`events.json` の構造：

```json
{
  "last_updated": "2026-03-19T00:00:00.000000",
  "total_events": 10,
  "events": [
    {
      "id": 1,
      "title": "イベント名",
      "date": "2026-04-10",
      "time": "18:30～20:30",
      "location": "東京都渋谷区",
      "description": "イベント説明",
      "category": "networking",
      "source_url": "https://...",
      "source_name": "JICA公式サイト",
      "collected_date": "2026-03-19T00:00:00.000000"
    }
  ]
}
```

## 🛠️ トラブルシューティング

### GitHub Actions でエラーが出る

1. ログを確認: Actions タブ → ワークフロー → 最新実行をクリック
2. よくあるエラー：
   - **認証エラー**: PAT（Personal Access Token）を確認
   - **スクレイピング失敗**: Webサイトの構造変更により対応が必要
   - **Python パッケージエラー**: `requirements.txt` を使用

### イベント情報が表示されない

1. `events.json` が正しく生成されているか確認
2. ブラウザの キャッシュをクリア
3. developer console でエラーを確認

## 📈 将来の拡張案

- [ ] 参加申込機能
- [ ] ユーザー登録・マイページ
- [ ] イベント通知機能（メール、LINE Bot）
- [ ] API化（他サイトから利用可能に）
- [ ] データベース連携（より高速な検索）
- [ ] Slack Bot 連携
- [ ] Google Calendar 連携

## 📄 ライセンス

MIT License - 自由に改変・配布できます

## 👥 貢献

改善案やバグ報告は Issue や Pull Request でお願いします。

## 📧 サポート

質問や問題がある場合は、GitHub Issues でお知らせください。

---

**最終更新**: 2026年3月19日
