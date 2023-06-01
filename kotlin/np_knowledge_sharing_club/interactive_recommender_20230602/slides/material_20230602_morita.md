---
format:
  revealjs:
    # incremental: false
    # theme: [default, custom_lab.scss]
    theme: [default, custom_lab.scss]
    slide-number: true
    logo: https://s3-ap-northeast-1.amazonaws.com/qiita-image-store/0/1697279/dfa905d1c1e242b4e39be182ae21a2b6ac72c0ad/large.png?1655951919
    footer: ⇒ [https://qiita.com/morinota](https://qiita.com/morinota)
from: markdown+emoji

fig-cap-location: bottom

title: ユーザとの対話で推薦結果を変化させるInteractive Recommenderをfeed-serverに実装してみようとした話
subtitle: (推薦システム × kotlin × OpenAI API の話)
date: 2023/06/02
author: NewsPicks Data/Algorithm unit インターン 森田大登
title-slide-attributes:
  #   data-background-image: https://i.imgur.com/nTazczH.png
  data-background-size: contain
  data-background-opacity: "0.5"
---

## このテーマを選んだ経緯

- 私はML分野、特に**推薦システム**やパーソナライズが好きです.
- 私のkotlin歴は4ヶ月程で、きっかけは業務で**feed-server**を触り始めた事です.(元々はML周りでPythonとRを嗜んでました.)
  - newspicks-feed-server は、メインフィードのあなたへのおすすめや各カテゴリセクション、フォローフィードで表示する記事リストを生成するサービスです.
  - NewsPicksにおいて推薦システムのコアロジックの学習はPythonですが、推論はkotlin(feed-server)で実装されています.
- また、**LLMやOpenAI API**が最近話題なので、関連した話だと皆さん楽しいかも...?

これらを踏まえて、**推薦システム × kotlin × LLM(OpenAI API)** という事で、「ユーザとの対話で推薦結果を変化させるInteractive Recommenderをfeed-serverに実装してみようとした話」にしました!

## 推薦システム × LLM で何ができそう??

推薦システムとは...

> 複数の候補からユーザにとって価値のあるものを選び出し、意思決定を支援するシステム
> (引用元: [推薦システム実践入門](https://www.oreilly.co.jp/books/9784873119663/))

「価値あるものを選び出すこと」「意思決定の支援」のどちらでも、LLMの活用で新たな価値創出ができるのでは?? [参考資料2]()では以下のアイデアを紹介...!

- 「価値あるものを選び出すこと」
  - 自然言語による対話を通じた**Interactiveな推薦結果の調節**.
  - 情報が不十分な新規ユーザのデータ拡張
- 「意思決定の支援」
  - 推薦結果の説明性(理由や根拠)の付与
  - 推薦後の心理的ハードルの高いアクションの支援(ex.NPで言えばコメント?)

## feed-server に Interactive Recommenderを実現するとしたら...{auto-animate=true}

今回は"あなたへのおすすめ"に表示する記事リストを、ユーザとの対話を通して変化(調整)させる機能を想定します.

現在は以下の様な手順で記事リストを生成しています.

- 1. np-serverからfeed-serverの`hogehoge` endpointにリクエストが送られる.
- 2. 指定されたユーザの推薦記事候補(`List<FeedUpdate>`)を取得する.
- 3. 推薦システムのコアロジックによって推薦記事候補を並び替えて、推薦記事ランキングを作る.
- 4. ヒューリスティックなランキング調整(ex. 過去に閲読した記事、古い記事のランクを下げる、etc.)
- 5. np-serverに推薦記事ランキングのレスポンスを返す.

## feed-server に Interactive Recommenderを実現するとしたら...{auto-animate=true}

今回は"あなたへのおすすめ"に表示する記事リストを、ユーザとの対話を通して変化(調整)させる機能を想定します.

Interactive Recommenderを実現する為に、ココをこうしてこうじゃ!

- 1. np-serverからfeed-serverの`hogehoge` endpointにリクエストが送られる.
- 2. 指定されたユーザの推薦記事候補(`List<FeedUpdate>`)を取得する.
- 3. **リクエストに含まれるユーザからのメッセージ`userChat`を用いて、推薦記事候補をフィルタリングする**.
- 4. 推薦システムのコアロジックによって推薦記事候補を並び替えて、推薦記事ランキングを作る.
- 5. ヒューリスティックなランキング調整(ex. 過去に閲読した記事、古い記事のランクを下げる、etc.)
- 6. np-serverに推薦記事ランキングのレスポンスを返す.

# さあやってみよう! まずはunit testを書くところから!

## `InteractiveRecommender` のtestはこんな感じ?

```kotlin:TestInteractiveRecommender.kt
package integrationTests

import InteractiveRecommender
import Item
import org.junit.jupiter.api.Test
import kotlin.test.assertEquals

class TestInteractiveRecommender {
    private val feedUpdates = listOf(
        Item("1", "政府、地方自治体に対しデジタル化支援金を交付", "finance", 0.6),
        Item("2", "日銀、マイナス金利を維持", "finance", 0.7),
        Item("3", "日本株式市場、急落", "finance", 0.8),
        Item("4", "米中貿易戦争の影響、新興市場に拡大", "business", 0.5),
        Item("5", "企業間の競争激化、IT業界にも波及", "technology", 0.8),
        Item("6", "景気減速、デフレリスク増加", "finance", 0.4),
        Item("7", "ブロックチェーン技術、急速に普及", "technology", 0.6),
        Item("8", "日本、TPPに復帰", "business", 0.7),
        Item("9", "ロボット革命により雇用機会が減少", "industry", 0.4),
        Item("10", "新しい産業革命の波が到来", "technology", 0.8)
    )

    @Test
    fun filteringRecommendationItemsByCategoryWhenGotRequestAboutCategory() {
        // Arrange
        val userComment = "金融に関するニュースに興味があります!"
        val sut = InteractiveRecommender()

        // Act
        val filteredUpdates = sut.recommend(feedUpdates, userComment)

        // Assert
        val filteredUpdatesExpected = listOf(
            Item("1", "政府、地方自治体に対しデジタル化支援金を交付", "finance", 0.6),
            Item("2", "日銀、マイナス金利を維持", "finance", 0.7),
            Item("3", "日本株式市場、急落", "finance", 0.8),
            Item("6", "景気減速、デフレリスク増加", "finance", 0.4)
        )
        assertEquals(filteredUpdatesExpected, filteredUpdates)
    }
}
```

## `TextToQueryConverter` のtestはこんな感じ?

```kotlin:TextToQueryConverterTest.kt
package integrationTests

import TextToQueryConverter
import kotlin.test.Test
import kotlin.test.assertEquals

class TestTextToQueryConverter {
    @Test
    fun whenUserSayRequestAboutCategoryItConvertToSQLQuery() {
        // Arrange
        val userChat = "私は金融の記事を読みたいです...!"
        val sut = TextToQueryConverter()

        // Act
        val query = sut.convert(userChat)

        // Assert
        assertEquals("SELECT * FROM items WHERE category = 'finance'", query)
    }
}
```

## `ItemFilterFromQuery` のtestはこんな感じ?

```kotlin:TestItemFilterFromQuery.kt
package integrationTests

import InteractiveRecommender
import Item
import org.junit.jupiter.api.Test
import kotlin.test.assertEquals

class TestInteractiveRecommender {
    private val feedUpdates = listOf(
        Item("1", "政府、地方自治体に対しデジタル化支援金を交付", "finance", 0.6),
        Item("2", "日銀、マイナス金利を維持", "finance", 0.7),
        Item("3", "日本株式市場、急落", "finance", 0.8),
        Item("4", "米中貿易戦争の影響、新興市場に拡大", "business", 0.5),
        Item("5", "企業間の競争激化、IT業界にも波及", "technology", 0.8),
        Item("6", "景気減速、デフレリスク増加", "finance", 0.4),
        Item("7", "ブロックチェーン技術、急速に普及", "technology", 0.6),
        Item("8", "日本、TPPに復帰", "business", 0.7),
        Item("9", "ロボット革命により雇用機会が減少", "industry", 0.4),
        Item("10", "新しい産業革命の波が到来", "technology", 0.8)
    )

    @Test
    fun filteringRecommendationItemsByCategoryWhenGotRequestAboutCategory() {
        // Arrange
        val userComment = "金融に関するニュースに興味があります!"
        val sut = InteractiveRecommender()

        // Act
        val filteredUpdates = sut.recommend(feedUpdates, userComment)

        // Assert
        val filteredUpdatesExpected = listOf(
            Item("1", "政府、地方自治体に対しデジタル化支援金を交付", "finance", 0.6),
            Item("2", "日銀、マイナス金利を維持", "finance", 0.7),
            Item("3", "日本株式市場、急落", "finance", 0.8),
            Item("6", "景気減速、デフレリスク増加", "finance", 0.4)
        )
        assertEquals(filteredUpdatesExpected, filteredUpdates)
    }
}
```

# さあ実装を作るぞ!

## `TextToQueryConverter` を実装するぞ!

```kotlin:TextToQueryConverter.kt
import kotlinx.serialization.Serializable
import kotlinx.serialization.decodeFromString
import kotlinx.serialization.json.Json
import okhttp3.OkHttpClient
import okhttp3.Request
import okhttp3.MediaType.Companion.toMediaType
import okhttp3.RequestBody.Companion.toRequestBody
import okhttp3.Response
import okhttp3.ResponseBody


class TextToQueryConverter {

    private val env: MutableMap<String, String> = System.getenv()
    private val apiKey = env["OPENAI_API_KEY"] ?: "empty"
    private val API_ENDPOINT = "https://api.openai.com/v1/chat/completions"
    private val PROMPT_TEMPLATE = """
        あなたの目的は、[ユーザからのコメント]を受け取って、itemsテーブルからユーザが求めるnewsレコードを取得できるようなSQLクエリを作る事です.
        itemsテーブルの各カラムの定義は以下に示します:
        - category(String): It is the category of the news article. unique values are [business, finance, career, education, technology, industry]
        - complexity(Float): It is the complexity of the news article. the value range is (0.0, 1.0). 1.0 means the most complicated. 0.0 is the simplest.

        出力形式は必ず SELECT * FROM items WHERE {} というSQLクエリの形式にしてください.
        あなたは[ユーザからのコメント]を受け取って、ユーザが求めるnewsを取得できるようなSQLクエリを作れるように、SQLクエリ内の{}をreplaceしてください.
        なお、使用して良いのはwhere句のみです. 単語やoperator間はwhitespaceで区切ってください.

        ではよろしくお願いいたします。今回の[ユーザからのコメント]は以下です: {userChat}
    """.trimIndent()
    private val REQUEST_BODY_TEMPLATE = """
        {
            "model": "gpt-3.5-turbo",
            "messages": [{"role": "user", "content": "{prompt}"}],
            "temperature": 0.7
        }
    """.trimIndent()

    fun convert(userChat: String): String? {
        val prompt = preparePrompt(userChat)
        val requestBodyString = REQUEST_BODY_TEMPLATE.replace("{prompt}", prompt)

        val response = requestToOpenaiApi(requestBodyString)

        return extractAnswer(response.body)
    }

    private fun preparePrompt(userChat: String): String {
        val prompt = PROMPT_TEMPLATE.replace("{userChat}", userChat)
        return prompt.replace("[\n\r]".toRegex(), "")
    }

    private fun requestToOpenaiApi(requestBodyString: String): Response {
        val client = OkHttpClient()
        val jsonMediaType = "application/json".toMediaType()

        val requestBody = requestBodyString.toRequestBody(jsonMediaType)
        val request = Request.Builder().url(API_ENDPOINT).header("Content-Type", "application/json")
            .header("Authorization", "Bearer $apiKey").post(requestBody).build()

        return client.newCall(request).execute()
    }

    private fun extractAnswer(responseBody: ResponseBody?): String? {
        val bodyString = responseBody?.string() ?: ""
        val json = Json { ignoreUnknownKeys = true }
        val parsedJson = json.decodeFromString<ChatCompletionResponse>(bodyString)
        return parsedJson.choices.firstOrNull()?.message?.content
    }
}

@Serializable
private data class ChatCompletionResponse(val choices: List<Choice>)


@Serializable
private data class Choice(val message: Message)

@Serializable
private data class Message(val content: String)

```

## `ItemFilterByQuery` を実装するぞ!

```kotlin:ItemFilterByQuery.kt
import net.sf.jsqlparser.expression.Expression
import net.sf.jsqlparser.expression.operators.conditional.AndExpression
import net.sf.jsqlparser.expression.operators.conditional.OrExpression
import net.sf.jsqlparser.expression.operators.conditional.XorExpression
import net.sf.jsqlparser.expression.operators.relational.ComparisonOperator
import net.sf.jsqlparser.expression.operators.relational.EqualsTo
import net.sf.jsqlparser.expression.operators.relational.GreaterThanEquals
import net.sf.jsqlparser.expression.operators.relational.MinorThanEquals
import net.sf.jsqlparser.parser.CCJSqlParserUtil
import net.sf.jsqlparser.statement.select.PlainSelect
import net.sf.jsqlparser.statement.select.Select
import net.sf.jsqlparser.statement.select.SelectBody

class ItemFilterByQuery {
    fun filter(sqlQuery: String, items: List<Item>): List<Item> {
        val statement = CCJSqlParserUtil.parse(sqlQuery)
        val select = statement as? Select
        val selectBody = select?.selectBody

        val whereClauseExpression = extractWhereClause(selectBody)
        if (whereClauseExpression == null) {
            println("This query doesn't include Comparison Operator. so return pure items.")
            return items
        }

        println("This query include Comparison Operator. so conduct items filtering.")
        return items.filter { isValidItemByExpression(it, whereClauseExpression) }
    }

    private fun isValidItemByExpression(item: Item, whereClause: Expression): Boolean {
        return when (whereClause) {
            is AndExpression -> filterItemByAndExpression(item, whereClause)
            is OrExpression -> filterItemByOrExpression(item, whereClause)
            is XorExpression -> filterItemByXorExpression(item, whereClause)
            else -> filterItemBySingleExpression(item, whereClause)
        }
    }

    private fun filterItemByAndExpression(item: Item, andExpression: AndExpression): Boolean {
        val isValidLeft = isValidItemByExpression(item, andExpression.leftExpression)
        val isValidRight = isValidItemByExpression(item, andExpression.rightExpression)
        return isValidLeft and isValidRight
    }

    private fun filterItemByOrExpression(item: Item, orExpression: OrExpression): Boolean {
        val isValidLeft = isValidItemByExpression(item, orExpression.leftExpression)
        val isValidRight = isValidItemByExpression(item, orExpression.rightExpression)
        return isValidLeft or isValidRight
    }

    private fun filterItemByXorExpression(item: Item, xorExpression: XorExpression): Boolean {
        val isValidLeft = isValidItemByExpression(item, xorExpression.leftExpression)
        val isValidRight = isValidItemByExpression(item, xorExpression.rightExpression)
        return isValidLeft xor isValidRight
    }

    private fun filterItemBySingleExpression(item: Item, singleExpression: Expression): Boolean {
        if (singleExpression !is ComparisonOperator) {
            return true
        }
        // ここにカラム名や演算子に基づいたフィルタリング処理を実装する
        val columnName = singleExpression.leftExpression.toString()
        val value = singleExpression.rightExpression.toString().replace("'", "") // 文字列に''が含まれてるので取り除く.

        if (singleExpression is EqualsTo) {
            when (columnName) {
                "category" -> return (item.category == value)
            }
        }
        if (singleExpression is GreaterThanEquals) {
            when (columnName) {
                "complexity" -> return (item.complexity >= value.toDouble())
            }
        }
        if (singleExpression is MinorThanEquals) {
            when (columnName) {
                "complexity" -> return (item.complexity <= value.toDouble())
            }
        }
        return true
    }

    private fun extractWhereClause(selectBody: SelectBody?): Expression? {
        if (selectBody !is PlainSelect) {
            return null
        }
        return selectBody.where
    }
}
```

## `InteractiveRecommender` を実装するぞ!

```kotlin:InteractiveRecommender.kt
class InteractiveRecommender {
    private val itemFilter = ItemFilterByQuery()
    private val textToQueryConverter = TextToQueryConverter()
    fun recommend(items: List<Item>, userChat: String): List<Item> {
        val sqlQuery = textToQueryConverter.convert(userChat)
        sqlQuery ?: return items
        return itemFilter.filter(sqlQuery, items)
    }
}
```

思った事:

- `ItemFilterByQuery`や`TextToQueryConverter`の初期化の仕方はどうすべきだろう...?:
  - `InteractiveRecommender` の中で初期化すべき?
  - それとも外部で初期化してコンストラクタの引数として渡すべき?

# いざfeed-serverにInteractive Recommenderを組み込むぞ!

## 計画はこうだ!

## と思ったが、あれ?

feed-serverの`gradle.build.kts`に必要なpackageの依存関係を定義してbuildを試みると...あれ?
kotlinのversionの問題でpackageをinstallできないんだろうか??:thinking:

という感じで、ココでタイムアップでした...!
(本当はdev環境にデプロイして、実際にranking endpointに`userChat` parameterを指定してリクエスト投げて...みたいなデモンストレーションがしたかったが...kotlin力 or gradle力不足...!)

## 終わりに...

- **推薦システム × kotlin × LLM(OpenAI API)** をテーマに、ユーザとの対話で推薦結果を変化させる**Interactive Recommender**をfeed-serverに実装を試みました!
  - 具体的には、「ユーザの自然言語を受け取る -> SQLクエリに変換 -> 推薦記事候補をフィルタリングする」処理をテスト・実装してみた.
  - feed-serverに組み込むプロセスでタイムアップし断念...!
- 得られた知見・感想:
  - 最近読んでる"単体テストの考え方/使い方"を参考にテストを書いてみたが、"観察可能な振る舞い"のみをテストする事を意識できた.
  - kotlinはpublicなmethodとprivateなmethodを明示的に定義できて嬉しいな...(Pythonが特殊なのかな)
  -

## 参考資料

- 1. [推薦システム実践入門](https://www.oreilly.co.jp/books/9784873119663/)
- 2. 「推薦システムに力を入れている」で(たぶん!)有名なWantedlyさんのData Scientistの方のLT資料: [LLMを活用した推薦システムの改善:課題と初期導入のアプローチ](https://speakerdeck.com/zerebom/llmwohuo-yong-sitatui-jian-sisutemunogai-shan-ke-ti-tochu-qi-dao-ru-noapuroti)
-
