## Caffeine Cache について

使い方の例:

```kotlin
private val cache: LoadingCache<Unit, List<OnboardingBanditParams>> = Caffeine.newBuilder()
        .refreshAfterWrite(getCacheRefreshInterval())
        .build { loadParamsFromS3() }
```

- `LoadingCache`は、キーに基づいて値を自動的にロードするキャッシュ。
  - 値はリスト型。
  - `Unit`はキーの型で、これは実質ダミーキーとして使用される。
    - i.e. つまりこのキャッシュは、「常に1つの固定キーに対して値をキャッシュする」 = **シンプルに1セットのパラメータをキャッシュしてるだけ**。
- `Caffeine.newBuilder()`で、キャッシュのビルダーを初期化。
- `.refreshAfterWrite(getCacheRefreshInterval())`メソッド:
  - 「データを書き込んだ後、指定した時間が経過したら、自動でリロード(再取得)する」設定。
  - `getCacheRefreshInterval()`はたぶんDurationを返す関数で、キャッシュの更新間隔を定義してるはず。
  - `refreshAfterWrite`は**非同期で再読み込み**をしてくれるので、古い値を即座に無効化せずに使い続けながら裏で更新してくれる。
  - 非同期読み込みが走るタイミング: 
    - エントリが更新から指定された時間が経過した後で、**次にキャッシュのgetが呼ばれた時**。その時に非同期でリロードされる。
- `.build { loadParamsFromS3() }`メソッド:
  - `build {...}`の中身は、「**キャッシュが存在しない or 更新する必要がある場合に呼ばれるローダー関数**」。

キャッシュへアクセスする時の例:

```kotlin
val params: List<OnboardingBanditParams> = cache.get(Unit)
```
