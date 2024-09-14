# docker container imageのサイズを小さくする戦略について調べる

## refs

- 同じ悩みを持ってる人がいた: [How do I slim down SBERT's sentencer-transformer library?](https://stackoverflow.com/questions/77205123/how-do-i-slim-down-sberts-sentencer-transformer-library)
- Pytorchのサイズを小さくする方法: [Poetry: Using PyTorch CPU (or other methods to reduce size) #1409](https://github.com/UKPLab/sentence-transformers/issues/1409)
- まだ読んでないけどsentence-transformersのissue: [Reduce 'sentence-transformer' package size #2319](https://github.com/UKPLab/sentence-transformers/issues/2319)
- M3さんのブログ: [Pythonの機械学習用Docker imageのサイズ削減方法の紹介](https://www.m3tech.blog/entry/reduce-python-docker-image-size)

## sentence-transformersを入れるとサイズがデカくなる問題

- 11GBくらいのコンテナイメージになってしまった。buildにもpushにもpullにも時間がかかるので、どうにかサイズを小さくしたい。
- 依存する`nvidia`と`torch`がデカいことが原因っぽい。
