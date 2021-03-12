# プロジェクトの始め方
```bash
docker-compose run django django-admin.py startproject (プロジェクト名) .
```



# サービス起動
```bash
$ make up
```
# サービス停止
```bash
$ make down
```

# フロントエンド開発開始
```bash
// mockサーバー (http://localhost:4010)
$ make front-mock
// localサーバー (http://localhost:8000)
$ make front-local
// 本番サーバー (http://b-map.pbl.jp)
$ make front-prod
```

# リンター起動（コード整形）
```
$ make front-lint
```

# ライブラリ追加
```
Vuejs
$ docker-compose exec node npm install vuelidate --save
```

# django

# DB設定
setting.pyのDATABASESの項目を以下の要領で編集
設定する値は，docker-composeで設定したものにすること
```bash:setting.py
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'django-db',
        'USER': 'django',
        'PASSWORD': 'django',
        'HOST': 'db',
        'PORT': '3306'
    }
}
```
# DB更新
```
make migrate
```
