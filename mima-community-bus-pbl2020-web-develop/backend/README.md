## バックエンド開発の始め方
### docker-composeの立ち上げ
```bash
make back-dev
```
### DBの作成およびモデル更新のDBへの適用
カレントディレクトリがbackendの場合
```bash
docker-compose exec django ./manage.py makemigration bus
docker-compose exec django ./manage.py migrate
```
### Oauth2認証サーバーの立ち上げ
```bash
docker-compose exec django ./manage.py migrate oauth2_provider
```
### テストデータの読み込み方
カレントディレクトリがbackendの場合
```bash
docker-compose exec django python manage.py loaddata bus/fixtures/*.json
```
カレントディレクトリがプロジェクトルートの場合
```bash
make back-seed
```
## トークンの取得の仕方
postmanを使って以下のURLにアクセス
```
http://localhost:8000/api/v1/login/
```
このときボディに以下のデータを入れておく
```{json}
{
    "email": "h847002y@mails.cc.ehime-u.ac.jp", 
    "password": "ictxict0"
}
```
得られたトークンはコピーしてpostmanのAuthorizationに設定して用いる

