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

### ジッターを使ったキャッシュ更新のランダム化

「キャッシュのリフレッシュ間隔に**ちょびっとランダム性（ジッター）**を加えて、アクセス集中を避ける」っていうテクニック

- ジッター(jitter)とは??
  - 元々の意味: 通信の用語。信号の到達タイミングのブレ（ゆらぎ）
  - ソフトウェアの文脈では、「**ある処理のタイミングをわざとランダムにずらす**」こと。
- なぜジッターが必要??
  - **全スレッドやプロセスが一斉にキャッシュ更新しにいくのを防ぐため!**
  - ex. 
    - 50スレッドが 30分ごとにS3アクセス！ ってなってたら、同時にS3へアクセス集中しちゃって、重くなる or エラーになりがち…
  - そこでジッター（ちょっとだけズラす）を入れることで→ **自然にアクセスがばらけて、システムが安定する！**
- ソフトウェア文脈でのジッターの使われどころ例:
  - 1. キャッシュの更新
  - 2. リトライ処理
  - 3. 定期ジョブやスケジューラー

```kotlin
// この値をrefreshAfterWrite()に指定するイメージ.
private fun getCacheRefreshInterval(): Duration {
        val jitterMinutes = ThreadLocalRandom.current().nextLong(0, 5)
        return CACHE_REFRESH_INTERVAL_MINUTES.plusMinutes(jitterMinutes)
    }
```

- `ThreadLocalRandom.current()` は、スレッド安全な乱数生成器を取得。
- `nextLong(0, 5)` は、0から4までのランダムな整数値を生成してる。
  - i.e. この`jitterMinutes`は、リフレッシュ間隔を微妙にずらすためのランダム時間!

