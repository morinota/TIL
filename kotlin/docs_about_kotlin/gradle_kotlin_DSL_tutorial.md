## 参考:

- [Spring Boot2 _ Kotlin _ Gradle5で、クリーンアーキテクチャのアプリケーションを構築する](https://radiochemical.hatenablog.com/entry/2019/09/08/164542)
- [Gradle Kotlin DSL入門](https://qiita.com/toliner/items/8b1ed6ed3cc04c22d63d)
- [Gradleでマルチプロジェクトを作成する.](https://zenn.dev/boronngo/articles/gradle-multi-project)

# Gradleについて:

- そもそもGradleってなんだっけ?:
  - オープンソースで開発されている**ビルド自動化ツール**.
  - Java, Kotlin, Scalaなど、JVM系の言語で書かれたモジュールのビルドツールとしてしばしば利用される.
  - JVM上で実行されるだけで、実はTypeScriptやGoのモジュールもプラグインを利用することでビルドできたりする.
  - Gradleでは、DSLとしてGroovyもしくはKotlinを利用して定義できる.

## Gradleの概念:

- project:
  - Gradleの**ビルド対象**のことを project と呼ぶ.
  - subprojectが無い場合は、**`build.gradle`ファイルがあるディレクトリ = 1つのprojectという扱い**になる.
  - project はネストさせたり(**ネストさせた project を subproject と呼ぶ**)、**依存関係を定義**してモジュール化する(multi module化)ことも可能.
    - subprojectを作ったりmulti module化する場合は、複数のbuild.gradle.ktsを作る必要がある? それともroot project のbuild.gradle.ktsにまとめて定義していける??
    - それぞれsubprojectのbuild.gradleファイルを定義した場合は、local pluginとして読み込める.
    - また、subproject間で依存関係を定義する場合は、読み込みしたいproject の `dependencies` に、読み込まれたい(依存されたい)projectを `implementation`で追加したら良さそう...!`implementation project(':application')`みたいな感じで定義してる...!
- task:
  - アプリケーション開発における**何かしらのタスクを実行するもの**.(ビルド、アプリ実行、テスト実行、デプロイ, etc.)
  - デフォルト(build-in)でも様々なタスクが組み込まれており、一般的な最低限のビルドのニーズを満たすようなものはだいたいある.
  - より高度なことを実現する場合は、後続で説明するプラグインを利用するか、DSLで自作のタスクを定義する.
- plugin:
  - プラグインを利用すると便利なタスクを追加できたり、ビルド自動化を超えたタスクを実行できる. (**Gradleにおける、packageやmoduleみたいな感じ...!**)
  - Gradleのpluginの例:
    - Ktlintを使ってktファイルにフォーマットをかける
    - SonarQubeで静的解析を行なう
    - サブプロジェクト毎に生成されるテストレポート・カバレッジをひとまとめにして閲覧できるようにする
  - 公開されているプラグインを利用することで、**ビルドの範疇外のタスク**を行なうことができる.

## Gradleで定義する事:

- plugins{}: gradle pluginの読み込み.
- repositories{}: サードパーティライブラリを利用する場合は、それをどこからダウンロードしてくるかの設定が必要.
- dependencies{}: サードパーティライブラリの読み込み.
  - `implementation`はproject配下の全パッケージ(全てのファイル)で、`testImplementation`はtest配下のパッケージでのみ、設定したライブラリを利用できる.
  - ここで、subproject間の依存関係の向きを定義してた!

## build.gradle.ktsを共通化する

- 全てのsubprojectで共通のライブラリを使用したい場合、それぞれのgradle定義に追加するのは冗長で面倒.
- ->Gradleには共通化(一元管理)する仕組みが用意されてる!
  - まずroot directory以下に`buildSrc`ディレクトリを追加. このディレクトリ名はGradleにとって特別なディレクトリ. なので名前の変更はできない!
  - buildSrc以下に、build.gradle.ktsを作成. 記載.
  - 続いて、ライブラリ情報を記載するkotlin objectを用意(`Hoge.kt`).
  - 
  - 

# Gradle Kotlin DSL 入門

## reference

- https://qiita.com/toliner/items/8b1ed6ed3cc04c22d63d

## なにそれ?

- Gradle Kotlin DSLはGradle 5.0で正式版になった、**GradleのビルドスクリプトをKotlinで書ける**機能.
  - build.gragle.ktsが、Kotlinで書かれたGradleビルドスクリプト...!
- 従来のビルドスクリプトであるbuild.gradleとsettings.gradleは、**Groovy**というJVM上で動作するスクリプト言語を用いていた.
  - しかしその時代は、Gradle Kotlin DSLの到来で終了した!
- **ビルドスクリプトとビルド対象のコードを両方Kotlinで書ける**事により、ビルドスクリプトの読解と編集の障壁は圧倒的に下がった...!
- しかし、現在、Gradle Kotlin DSLについての日本語での入門記事はあまりない. また、**GradleのAPIとGradle Kotlin DSL特有のAPIが混在する**ため、学習に難易度がやや高い.

## 実際に見てみる

現バージョンでIntellijにより自動生成されるKotlinのバージョンは以下のような感じ.

```
plugins {
    kotlin("jvm") version "1.3.61"
}

group = "org.example"
version = "1.0-SNAPSHOT"

repositories {
    mavenCentral()
}

dependencies {
    implementation(kotlin("stdlib-jdk8"))
}

tasks {
    compileKotlin {
        kotlinOptions.jvmTarget = "1.8"
    }
    compileTestKotlin {
        kotlinOptions.jvmTarget = "1.8"
    }
}
```

上から順に見ていく.

### `plugin{}`:

- `kotlin()`という、Groovy版には無い専用関数でKotlinのPluginを指定している.
- Pluginのバージョンを指定する為に、 `version` infix関数を使用.

以下のような感じで、pluginを指定できる.(packageをimportしてるみたいなイメージ...!)

```kotlin
plugins {
    kotlin("jvm") version "1.3.61"
    application
    `maven-publish`
    id("com.jfrog.bintray") version "1.8.4"
}
```

###
