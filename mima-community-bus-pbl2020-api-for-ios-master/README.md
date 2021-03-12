# Mimap API
watch here

https://ictc.github.io/mima-community-bus-pbl2020-api-for-ios/

# requirements
- node
- npm

# マージする前にやること
```
make concat
make build

動作チェック用で
make mock
```
# How to Use
## installation
- `npm install -g aglio`

## build
- `aglio -i index.apib -o index.html`

## watch
- `aglio -i index.apib -s`

# Build using docker
```
docker-compose up -d
docker-compose exec api bash
./node_modules/.bin/aglio -i index.apib -o index.html
```
## build
```
docker-compose exec api aglio -i index.apib -o index.html
```


# api for iOS App
- ログイン認証
- バス点検情報保存
- バスロケーション保存
- 乗降者数保存（乗降者数＋トリップーメータの値（オプショナル））
- 車両一覧取得API
- 点検項目取得API
- 便一覧取得API
- 路線一覧取得API
- 運行初期情報保存API
- バス停一覧取得API（路線を指定して，バス停一覧）
- 運賃一覧取得API
- 見守り登録API（画面タッチ時）

# Start mock server
```
docker-compose up -d --build
docker-compose exec api bash
```

まとめて起動！
```
./concat_all.sh
drakov -f all_api.apib --public --watch
```

例）立ち上げたいAPImockサーバーを個別に起動
```
drakov -f all_api.apib --public --watch
```

APIリクエスト例
```
curl -H GET 'http://localhost:3000/user/info' -H 'Content-Type:application/json;charset=utf-8' -H 'Authorization: Bearer {token}'
curl -H GET 'http://ictx01.ict.ehime-u.ac.jp:3000/user/info' -H 'Content-Type:application/json;charset=utf-8' -H 'Authorization: Bearer {token}'
```
response
```
{
  "id": "1",
  "name": "ehimeict",
  "phone_number": "08038473847",
  "email": "ehimeict@gmail.com"
}
```
