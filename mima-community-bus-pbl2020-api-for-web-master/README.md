# document

https://ictc.github.io/mima-community-bus-pbl2020-api-for-web/redoc-static.html

# requirements
- node
- npm

# install prism
```
npm install -g @stoplight/prism-cli
```

# start mock server
```
prism mock reference/mima-community-bus-pbl2020-web.v1.yaml
```


# build html
## install redoc-cli
```
npm install -g redoc-cli
```

## build
```
redoc-cli bundle reference/mima-community-bus-pbl2020-web.v1.yaml
```