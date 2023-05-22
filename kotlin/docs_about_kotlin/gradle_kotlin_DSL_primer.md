## link

https://docs.gradle.org/current/userguide/kotlin_dsl.html

# title

Gradle Kotlin DSL Primer

Gradle’s Kotlin DSL provides an alternative syntax to the traditional Groovy DSL with an enhanced editing experience in supported IDEs, with superior content assist, refactoring, documentation, and more. This chapter provides details of the main Kotlin DSL constructs and how to use it to interact with the Gradle API.
GradleのKotlin DSLは、従来のGroovy DSLの代替構文として、サポートされているIDEでの編集体験を強化し、優れたコンテンツアシスト、リファクタリング、ドキュメントなどの機能を提供します。この章では、主なKotlin DSLの構成の詳細と、それを使用してGradle APIと対話する方法について説明します。

If you are interested in migrating an existing Gradle build to the Kotlin DSL, please also check out the dedicated migration section.
既存のGradleビルドをKotlin DSLに移行することに興味がある場合は、専用の移行セクションもチェックしてください。

## Prerequisites

The embedded Kotlin compiler is known to work on Linux, macOS, Windows, Cygwin, FreeBSD and Solaris on x86-64 architectures.

Knowledge of Kotlin syntax and basic language features is very helpful. The Kotlin reference documentation and Kotlin Koans will help you to learn the basics.

Use of the plugins {} block to declare Gradle plugins significantly improves the editing experience and is highly recommended.F

# Kotlin DSL Scripts

Just like the Groovy-based equivalent, the Kotlin DSL is implemented on top of Gradle’s Java API. Everything you can read in a Kotlin DSL script is Kotlin code compiled and executed by Gradle. Many of the objects, functions and properties you use in your build scripts come from the Gradle API and the APIs of the applied plugins.
Groovyベースの同等品と同様に、Kotlin DSLはGradleのJava APIの上に実装されています。Kotlin DSLスクリプトで読むことができるものはすべて、Gradleによってコンパイルされ実行されるKotlinコードです。ビルドスクリプトで使用するオブジェクト、関数、プロパティの多くは、Gradle APIと適用されるプラグインのAPIから提供されます。

- Groovy DSL script files use the `.gradle` file name extension.
- Kotlin DSL script files use the `.gradle.kts` file name extension.

Kotlin DSLを有効にするには、ビルドスクリプトの拡張子を.gradleの代わりに.gradle.ktsにするだけです。これは、設定ファイル（例えばsettings.gradle.kts）と初期化スクリプトにも適用されます。

つまり、Kotlin DSLのビルドスクリプトはGroovy DSLのビルドスクリプトを適用することができ、マルチプロジェクトビルドの各プロジェクトはどちらかを使うことができます。
