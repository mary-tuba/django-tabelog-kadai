# NAGOYAMESHI - Django食べログ課題

名古屋B級グルメに特化したレビューアプリ「NAGOYAMESHI」

## 開発環境セットアップ

### 仮想環境のアクティベート
```bash
source kadai_002/nagoyameshi/bin/activate
```

### パッケージインストール
```bash
pip install django
pip install django-allauth  # メール認証用
pip install stripe          # 決済システム用
pip install Pillow          # 画像処理用
```

## プロジェクト構成設計

### Djangoアプリケーション構成
```
nagoyameshi/
├── manage.py
├── nagoyameshi/         # メインプロジェクト
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── accounts/            # ユーザー認証・管理
├── restaurants/         # 店舗管理
├── reviews/            # レビュー管理
├── reservations/       # 予約管理
├── payments/           # 決済管理
├── categories/         # カテゴリ管理
├── admin_panel/        # 管理者機能
└── static/            # 静的ファイル
```

### 各アプリケーションの役割

**accounts** - ユーザー管理
- 会員登録・ログイン・ログアウト
- プロフィール管理・編集
- 無料/有料会員の区別
- メール認証機能

**restaurants** - 店舗管理
- 店舗情報の管理（CRUD）
- 店舗検索・フィルタリング
- カテゴリ分類

**reviews** - レビューシステム
- レビュー投稿・編集・削除
- 星評価システム
- 無料会員は最新5件のみ表示制限

**reservations** - 予約管理
- 予約作成・確認・キャンセル
- 予約確認メール送信

**payments** - 決済システム
- Stripe連携でクレジットカード決済
- サブスクリプション管理（月額300円）

**categories** - カテゴリ管理
- 和食、洋食、手羽先、カレーなどの管理

**admin_panel** - 管理者機能
- 店舗管理・会員管理・売上管理
- レビュー削除・非公開機能

## データベース設計

### 主要なモデル

**User (CustomUser)** - カスタムユーザーモデル
- 名前、メール、パスワード、電話番号、住所
- is_premium（有料会員フラグ）

**Restaurant** - 店舗モデル
- 店舗名、住所、電話番号、画像、説明
- 平均予算、営業時間、定休日
- category (外部キー)

**Category** - カテゴリモデル
- カテゴリ名（和食、洋食など）

**Review** - レビューモデル
- user, restaurant (外部キー)
- 星評価、コメント、投稿日

**Reservation** - 予約モデル  
- user, restaurant (外部キー)
- 予約日、時間、人数

**Favorite** - お気に入りモデル
- user, restaurant (外部キー)

**Subscription** - サブスクリプションモデル
- user (外部キー)
- Stripe関連情報

## 認証・権限システム

- **django-allauth** でメール認証
- カスタムユーザーモデル（AbstractUser継承）
- 権限レベル：
  - 一般ユーザー（無料会員）
  - プレミアム会員（有料会員）
  - 管理者（店舗オーナー含む）

## 実装優先順位

1. **基本セットアップ**（Djangoプロジェクト作成）
2. **認証システム**（ユーザー登録・ログイン）
3. **店舗機能**（店舗表示・検索）
4. **レビュー機能**（投稿・表示制限）
5. **予約機能**
6. **決済システム**（Stripe連携）
7. **管理者機能**

## 機能制限

### 無料会員
- 最新レビューの5件のみ閲覧可能
- レビュー投稿不可
- 予約機能不可
- お気に入り機能不可

### 有料会員（月額300円）
- 全機能利用可能
- レビュー投稿・編集・削除
- 予約機能
- お気に入り機能
- 予約確認メール送信

## URL設計
```python
# メインurls.py
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('restaurants.urls')),  # トップページ
    path('accounts/', include('accounts.urls')),
    path('restaurants/', include('restaurants.urls')),
    path('reviews/', include('reviews.urls')),
    path('reservations/', include('reservations.urls')),
    path('payments/', include('payments.urls')),
    path('admin-panel/', include('admin_panel.urls')),
]
```

## 実装進捗

### ✅ 完了した作業

#### 2025-09-01
- [x] Djangoプロジェクト作成
  - `django-admin startproject nagoyameshi_project` 実行
  - プロジェクト構造確認完了
- [x] 必要なDjangoアプリケーション作成
  - `accounts` - ユーザー認証・管理
  - `restaurants` - 店舗管理
  - `reviews` - レビュー管理
  - `reservations` - 予約管理
  - `payments` - 決済管理
  - `categories` - カテゴリ管理
  - `admin_panel` - 管理者機能
- [x] 基本settings.py設定
  - 作成したアプリをINSTALLED_APPSに追加
  - 言語設定を日本語に変更 (ja)
  - タイムゾーンを東京に設定 (Asia/Tokyo)
  - 静的ファイルとメディアファイルの設定
- [x] カスタムユーザーモデル作成
  - AbstractUserを継承したUserモデル作成
  - フリガナ、住所、電話番号などの追加フィールド
  - is_premium（プレミアム会員）フラグ追加
  - email_verified（メール認証）フラグ追加
  - AUTH_USER_MODEL設定をsettings.pyに追加
  - 管理画面での表示設定（admin.py）

- [x] 基本的なURL設定
  - メインプロジェクトのurls.py設定
  - 各アプリのurls.py作成（accounts, restaurants, reviews, reservations, payments, categories, admin_panel）
  - メディアファイルと静的ファイルの配信設定
- [x] 基本的なビューとテンプレート作成
  - Bootstrapを使用したレスポンシブなベーステンプレート
  - restaurants: トップページ、店舗詳細、検索ページ
  - accounts: ログイン、会員登録、プロフィールページ
  - 全アプリの基本的なダミービュー実装
  - ナビゲーション、メッセージ表示、フッター実装

- [x] データベースマイグレーション実行
  - カスタムユーザーモデルのマイグレーション作成・実行
  - Djangoデフォルトテーブル作成完了
  - 静的ファイルディレクトリ作成
  - URL重複警告修正
- [x] スーパーユーザー作成
  - 管理者アカウント作成完了
  - 認証情報は `admin_credentials.txt` に記載

- [x] 基本モデル作成
  - Category: 料理カテゴリモデル
  - Restaurant: 店舗モデル（予算、営業時間、画像対応）
  - Review: レビューモデル（1-5星評価、コメント）
  - Reservation: 予約モデル（日時、人数、ステータス管理）
  - Favorite: お気に入りモデル
  - Subscription: サブスクリプションモデル（Stripe対応）
  - PaymentHistory: 決済履歴モデル

- [x] 新しいモデルのマイグレーション実行
  - Pillowライブラリインストール（画像対応）
  - makemigrationsでマイグレーションファイル作成
  - migrate実行でデータベーステーブル作成完了

- [x] 管理画面設定完了
  - 全モデルのDjango Admin設定
  - リスト表示、検索、フィルター機能設定
  - 編集可能フィールド設定

- [x] 開発環境動作確認
  - システムチェック実行（エラーなし）
  - データベース接続確認完了

### ✅ 基本システム構築完了

#### 2025-09-01 完了した追加作業
- [x] 全基本モデル実装完了
- [x] データベースマイグレーション完了
- [x] Django Admin管理画面設定完了
- [x] 開発環境動作確認完了

### 🚧 次の開発フェーズ

## データベース設定

### マイグレーション手順

1. **仮想環境をアクティベート**
   ```bash
   source kadai_002/nagoyameshi/bin/activate
   ```

2. **プロジェクトディレクトリに移動**
   ```bash
   cd kadai_002/nagoyameshi_project
   ```

3. **マイグレーションファイル作成**
   ```bash
   python manage.py makemigrations
   ```

4. **マイグレーション実行**
   ```bash
   python manage.py migrate
   ```

5. **スーパーユーザー作成**
   ```bash
   python manage.py createsuperuser
   ```

6. **開発サーバー起動**
   ```bash
   python manage.py runserver
   ```

### データベースファイル
- SQLiteファイル: `db.sqlite3`
- 管理画面URL: `http://127.0.0.1:8000/admin/`

### 📋 次に実装予定

1. **アプリケーション作成**
   ```bash
   python manage.py startapp accounts
   python manage.py startapp restaurants  
   python manage.py startapp reviews
   python manage.py startapp reservations
   python manage.py startapp payments
   python manage.py startapp categories
   python manage.py startapp admin_panel
   ```

2. **settings.py基本設定**
3. **カスタムユーザーモデル実装**
4. **データベース初期設定**