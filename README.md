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

## Herokuデプロイ設定

### settings.py修正内容

1. **ALLOWED_HOSTSの設定**
   ```python
   ALLOWED_HOSTS = ['localhost', '127.0.0.1', '.herokuapp.com']
   ```

2. **WhiteNoiseミドルウェア追加**（静的ファイル配信用）
   ```python
   MIDDLEWARE = [
       'django.middleware.security.SecurityMiddleware',
       'whitenoise.middleware.WhiteNoiseMiddleware',  # Heroku静的ファイル対応
       'django.contrib.sessions.middleware.SessionMiddleware',
       # その他のミドルウェア...
   ]
   ```

3. **静的ファイル設定**
   ```python
   STATIC_URL = '/static/'
   
   # Heroku静的ファイル対応
   STATIC_ROOT = BASE_DIR / 'static'
   STATICFILES_DIRS = [
       BASE_DIR / 'staticfiles',
   ]
   ```

### Herokuデプロイ手順

1. **必要なパッケージインストール**
   ```bash
   pip install whitenoise  # 静的ファイル配信用
   pip install gunicorn    # WSGIサーバー
   pip install psycopg2    # PostgreSQL接続用（本番環境）
   ```

2. **requirements.txt作成**
   ```bash
   pip freeze > requirements.txt
   ```

3. **Procfile作成**
   ```
   web: gunicorn nagoyameshi_project.wsgi
   ```

4. **runtime.txt作成**（Pythonバージョン指定）
   ```
   python-3.13.0
   ```

5. **Herokuログイン**
   ```bash
   heroku login
   ```

6. **Herokuアプリ作成**
   ```bash
   heroku create your-app-name
   ```

7. **環境変数設定**
   ```bash
   heroku config:set DEBUG=False
   heroku config:set SECRET_KEY=your-secret-key
   ```

8. **必要なパッケージの仮想環境での確認とrequirements.txt更新**
   ```bash
   # 仮想環境をアクティベート
   source kadai_002/nagoyameshi/bin/activate
   
   # プロジェクトディレクトリに移動
   cd kadai_002/nagoyameshi_project
   
   # 完全なrequirements.txtを生成
   pip freeze > requirements.txt
   
   # gitルートにコピー
   cd ../..
   cp kadai_002/nagoyameshi_project/requirements.txt .
   ```

9. **Pythonビルドパック設定**
   ```bash
   heroku buildpacks:set heroku/python --app nagoyameshi-20250902
   ```

10. **デプロイ実行**
    ```bash
    git add .
    git commit -m "Update requirements.txt with all dependencies including Django"
    git push heroku main
    ```

11. **データベースマイグレーション実行**
    ```bash
    heroku run python kadai_002/nagoyameshi_project/manage.py migrate --app nagoyameshi-20250902
    ```

### ✅ Herokuデプロイ完了

#### 2025-09-02 デプロイ成功
- **アプリURL**: https://nagoyameshi-20250902-46d577cc9c6d.herokuapp.com/
- **Herokuアプリ名**: nagoyameshi-20250902
- **使用データベース**: JawsDB MariaDB (MySQL互換)
- **Python バージョン**: 3.13.1

#### 実行済み作業
- [x] settings.pyのHeroku対応（ALLOWED_HOSTS, WhiteNoise, 静的ファイル設定）
- [x] Procfile作成（`web: gunicorn nagoyameshi_project.wsgi --log-file -`）
- [x] runtime.txt作成（Python 3.13.1指定）
- [x] requirements.txt作成（Django, gunicorn, whitenoise等含む）
- [x] JawsDB MariaDBアドオン追加
- [x] データベース環境変数設定
- [x] Herokuデプロイ実行
- [x] データベースマイグレーション実行

#### 設定済み環境変数
```bash
DB_HOST=z1ntn1zv0f1qbh8u.cbetxkdyhwsb.us-east-1.rds.amazonaws.com
DB_DATABASE=djo0z6j9h2csgffk
DB_USERNAME=fztcuwvx97eudjjz
DB_PASSWORD=ic4dze3sncnc5v1z
```

#### トラブルシューティング履歴
1. **buildpack検出失敗** → Pythonビルドパック手動設定で解決
2. **requirements.txtの場所** → gitルートディレクトリに配置で解決
3. **Django未インストール** → 仮想環境からの完全なrequirements.txt生成で解決

### 📋 次の開発フェーズ

1. **本番用settings.pyの最適化**
   - DEBUG=Falseの設定
   - セキュリティ設定の強化
   
2. **静的ファイル最適化**
   - collectstaticの警告解決
   
3. **スーパーユーザー作成**
   ```bash
   heroku run python kadai_002/nagoyameshi_project/manage.py createsuperuser --app nagoyameshi-20250902
   ```