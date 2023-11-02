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

title: ユーザとの対話で推薦結果を変化させるInteractiveなRecommenderをkotlinで実装してみようとした話
subtitle: (推薦システム × kotlin × OpenAI API の話)
date: 2023/06/02
author: morinota
title-slide-attributes:
  #   data-background-image: https://i.imgur.com/nTazczH.png
  data-background-size: contain
  data-background-opacity: "0.5"
---

## このテーマを選んだきっかけ

- 私はML分野、特に**推薦システム**やパーソナライズが好きです.
- 私のkotlin歴は4ヶ月程です.(元々はML周りでPythonとRを嗜んでました.)
- また、**LLMやOpenAI API**が最近話題なので、関連した話だと皆さん楽しいかも...?

これらを踏まえて、**推薦システム × kotlin × LLM(OpenAI API)** という事で、「ユーザとの対話で推薦結果を変化させるInteractive Recommenderをkotlin実装してみようとした話」をテーマに選びました.

## 推薦システム × LLM で何ができそう??

推薦システムとは...

> 複数の候補からユーザにとって価値のあるものを選び出し、意思決定を支援するシステム
> (引用元: [推薦システム実践入門](https://www.oreilly.co.jp/books/9784873119663/))

「価値あるものを選び出すこと」「意思決定の支援」のどちらでも、LLMの活用で新たな価値創出ができるのでは?? [参考2](https://speakerdeck.com/zerebom/llmwohuo-yong-sitatui-jian-sisutemunogai-shan-ke-ti-tochu-qi-dao-ru-noapuroti)では以下のアイデアを紹介されてました...!

- 「価値あるものを選び出すこと」
  - 自然言語による対話を通じた**Interactiveな推薦結果の調節**.
  - 情報が不十分な新規ユーザのデータ拡張
- 「意思決定の支援」
  - 推薦結果の説明性(理由や根拠)の付与
  - 推薦後の心理的ハードルの高いアクションの支援

# 架空のケーススタディ

今回は「**user_idを指定してリクエストを投げると、そのユーザにPersonalizeされた推薦アイテムリストを返す**」様な推薦サーバがkotlinで実装されている、と想定しましょう.

そして、推薦サーバに新たに「**ユーザとの対話を通して推薦アイテムを変化(調整)させる**」interactive recommender APIを追加する事を妄想しましょう...!

じゃあ何を推薦するか、と言うと、そうですね...ニュース！**ニュース記事**にしましょう!!
情報で溢れた現代社会において、ユーザにとって有用な情報と効率良く出会える様な、素敵な推薦システムを目指しましょう...!!

## 架空の推薦サーバAPIの振る舞い{auto-animate=true}

推薦サーバはリクエストを受けとった後、以下の様な手順でレスポンスを生成します.(一般的な推薦システムの構成ってこんな感じの印象...! 少し前に公開されたTwitterの推薦システムとかも...!)

- 1. 指定されたユーザの推薦アイテム候補(`List<Candidate>`)を取得する.(`Map<userId, List<Candidate>>`の形式でメモリキャッシュされてる)
- 2. 推薦システムのコアロジックによって推薦アイテム候補を並び替えて、推薦アイテムランキングを作る.
- 3. ヒューリスティックなランキング調整(ex. 過去に推薦済みのアイテム、古いアイテムのランクを下げる、etc.)
- 4. 推薦アイテムランキングをレスポンスとして返す.

Interactive Recommenderを実現する為に、ココをこうしてこうじゃ!

## 追加すべきInteractive Recommender APIの振る舞い {auto-animate=true}

変更された手順が以下じゃ!

- 1. 指定されたユーザの推薦アイテム候補(`List<Candidate>`)を取得する.(`Map<userId, List<Candidate>>`の形式でメモリキャッシュされてる)
- 2. **リクエストに含まれるユーザからのメッセージ`userChat`を用いて、推薦アイテム候補をフィルタリングする**.
- 3. 推薦システムのコアロジックによって推薦アイテム候補を並び替えて、推薦アイテムランキングを作る.
- 4. ヒューリスティックなランキング調整(ex. 過去に推薦済みのアイテム、古いアイテムのランクを下げる、etc.)
- 5. 推薦アイテムランキングをレスポンスとして返す.

## 推薦アイテム候補の属性情報の設定

今回は推薦アイテム候補に、記事のカテゴリと記事の複雑度(専門性の高さ)の属性情報が含まれているケースを想定しました.

```kotlin
data class Candidate(
    val id: String,
    val title: String,
    val category: String, // 記事カテゴリ(business, finance, career, eduacition, technology, industry の6種)
    val complexity: Double,
)
```

# さあやってみよう! まずはunit testを書くところから!

追加された手順「リクエストに含まれるユーザからのメッセージ`userChat`を用いて、推薦アイテム候補(`List<Candidate>`)をフィルタリングする.」処理のテスト & 実装を試みます...!

## `InteractiveRecommender` のtestはこんな感じ?

:::: {.columns}

::: {.column width="30%"}

InteractiveRecommenderの"観察可能な振る舞い"は、ユーザから入力される自然言語(`userChat`)を考慮して、推薦記事候補(`feedUpdates`)をフィルタリングする事です.

:::

::: {.column width="70%"}

```kotlin:TestInteractiveRecommender.kt
package integrationTests

import InteractiveRecommender
import Candidate
import org.junit.jupiter.api.Test
import kotlin.test.assertEquals

class TestInteractiveRecommender {
    private val candidates = listOf(
        Candidate("1", "政府、地方自治体に対しデジタル化支援金を交付", "finance", 0.6),
        Candidate("2", "日銀、マイナス金利を維持", "finance", 0.7),
        Candidate("3", "日本株式市場、急落", "finance", 0.8),
        Candidate("4", "米中貿易戦争の影響、新興市場に拡大", "business", 0.5),
        Candidate("5", "企業間の競争激化、IT業界にも波及", "technology", 0.8),
        Candidate("6", "景気減速、デフレリスク増加", "finance", 0.4),
        Candidate("7", "ブロックチェーン技術、急速に普及", "technology", 0.6),
        Candidate("8", "日本、TPPに復帰", "business", 0.7),
        Candidate("9", "ロボット革命により雇用機会が減少", "industry", 0.4),
        Candidate("10", "新しい産業革命の波が到来", "technology", 0.8)
    )

    @Test
    fun filteringRecommendCandidatesByCategoryWhenGotRequestAboutCategory() {
        // Arrange
        val userComment = "金融に関するニュースに興味があります!"
        val sut = InteractiveRecommender()

        // Act
        val filteredUpdates = sut.recommend(candidates, userComment)

        // Assert
        val filteredUpdatesExpected = listOf(
            Candidate("1", "政府、地方自治体に対しデジタル化支援金を交付", "finance", 0.6),
            Candidate("2", "日銀、マイナス金利を維持", "finance", 0.7),
            Candidate("3", "日本株式市場、急落", "finance", 0.8),
            Candidate("6", "景気減速、デフレリスク増加", "finance", 0.4)
        )
        assertEquals(filteredUpdatesExpected, filteredUpdates)
    }
}
```

:::

::::

## `InteractiveRecommender` の実装はこんな感じ?

- `InteractiveRecommender`内では、`TextToQueryConverter`と`CandidateFilterByQuery`が処理を実行します.(アプリケーションサービスとドメインモデルみたいな感じ)
- `CandidateFilterByQuery`や`TextToQueryConverter`の初期化の仕方はどうすべきだろう...?:
  - `InteractiveRecommender` の中で初期化すべき?
  - それともInterfaceをコンストラクタの引数として渡すべき?

```kotlin:InteractiveRecommender.kt
class InteractiveRecommender {
    private val candidateFilter = CandidateFilterByQuery()
    private val textToQueryConverter = TextToQueryConverter()
    fun recommend(candidates: List<Candidate>, userChat: String): List<Candidate> {
        val sqlQuery = textToQueryConverter.convert(userChat)
        sqlQuery ?: return candidates
        return candidateFilter.filter(sqlQuery, candidates)
    }
}
```

## `TextToQueryConverter` のtestはこんな感じ?

:::: {.columns}

::: {.column width="70%"}

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

:::

::: {.column width="30%"}

`TextToQueryConverter` の"観察可能な振る舞い"は、ユーザから入力される自然言語(`userChat`)をsqlクエリに変換する事です.

:::

::::

## `TextToQueryConverter` の実装はこんな感じ?

:::: {.columns}

::: {.column width="30%"}

ユーザから入力される自然言語(`userChat`)をクエリに変換する処理は、OpenAI APIの `chat` endpointに任せます.
特にpromptを練ることはなく、zero shot learning で推論してもらいました.
受け取ったレスポンスは`kotlinx.serialization`パッケージを用いてparseして変換後のクエリを取得しています.

:::

::: {.column width="70%"}

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

:::

::::

## `CandidateFilterByQuery` のtestはこんな感じ?

:::: {.columns}

::: {.column width="70%"}

```kotlin:TestCandidateFilterByQuery.kt
package unitTests

import CandidateFilterByQuery
import Candidate
import org.junit.jupiter.api.Test
import kotlin.test.assertEquals

class TestCandidateFilterByQuery {
    private val candidates = listOf(
        Candidate("1", "政府、地方自治体に対しデジタル化支援金を交付", "finance", 0.6),
        Candidate("2", "日銀、マイナス金利を維持", "finance", 0.7),
        Candidate("3", "日本株式市場、急落", "finance", 0.8),
        Candidate("4", "米中貿易戦争の影響、新興市場に拡大", "business", 0.5),
        Candidate("5", "企業間の競争激化、IT業界にも波及", "technology", 0.8),
        Candidate("6", "景気減速、デフレリスク増加", "finance", 0.4),
        Candidate("7", "ブロックチェーン技術、急速に普及", "technology", 0.6),
        Candidate("8", "日本、TPPに復帰", "business", 0.7),
        Candidate("9", "ロボット革命により雇用機会が減少", "industry", 0.4),
        Candidate("10", "新しい産業革命の波が到来", "technology", 0.8)
    )

    @Test
    fun candidatesAreStableWhenSqlQueryDontIncludeWhereClause() {
        // Arrange
        val sqlQuery = "SELECT * FROM items"
        val sut = CandidateFilterByQuery()

        // Act
        val filteredCandidates = sut.filter(sqlQuery, this.candidates)

        // Assert
        val filteredCandidatesExpected = this.candidates
        assertEquals(filteredCandidatesExpected, filteredCandidates)
    }

    @Test
    fun candidatesAreFilteredWhenSqlQueryIncludeWhereClauseAndEqualOperator() {
        // Arrange
        val sqlQuery = "SELECT * FROM items WHERE category = 'finance'"
        val sut = CandidateFilterByQuery()

        // Act
        val filteredCandidates = sut.filter(sqlQuery, this.candidates)

        // Assert
        val filteredCandidatesExpected = listOf(
            Candidate("1", "政府、地方自治体に対しデジタル化支援金を交付", "finance", 0.6),
            Candidate("2", "日銀、マイナス金利を維持", "finance", 0.7),
            Candidate("3", "日本株式市場、急落", "finance", 0.8),
            Candidate("6", "景気減速、デフレリスク増加", "finance", 0.4)
        )
        assertEquals(filteredCandidatesExpected, filteredCandidates)
    }

    @Test
    fun candidatesAreFilteredBySqlQueryIncludingWhereClauseAndGreaterthanEqualsOperator() {
        // Arrange
        val sqlQuery = "SELECT * FROM items WHERE complexity <=0.5"
        val sut = CandidateFilterByQuery()

        // Act
        val filteredCandidates = sut.filter(sqlQuery, this.candidates)

        // Assert
        val filteredCandidatesExpected = listOf(
            "米中貿易戦争の影響、新興市場に拡大",
            "景気減速、デフレリスク増加",
            "ロボット革命により雇用機会が減少",
        )
        assertEquals(filteredCandidatesExpected, filteredCandidates.map { it.title })
    }

    @Test
    fun candidatesAreFilteredBySqlQueryIncludingWhereClauseAndMultiOperators() {
        // Arrange
        val sqlQuery = "SELECT * FROM items WHERE category = 'finance' and complexity <=0.5 and complexity>=0.3"
        val sut = CandidateFilterByQuery()

        // Act
        val filteredCandidates = sut.filter(sqlQuery, this.candidates)

        // Assert
        val filteredCandidatesExpected = listOf(
            "景気減速、デフレリスク増加",
        )
        assertEquals(filteredCandidatesExpected, filteredCandidates.map { it.title })
    }
}
```

:::

::: {.column width="30%"}

`CandidateFilterByQuery` の"観察可能な振る舞い"は、sqlクエリに従って、メモリ上の推薦アイテム候補(`List<Candidate>`)をフィルタリングする事です.

:::

::::

## `CandidateFilterByQuery` の実装はこんな感じ?

:::: {.columns}

::: {.column width="30%"}

推薦アイテム候補(`List<Candidate>`)にsqlクエリを適用する為に、`jsqlparser`でクエリを構文解析する点が、この実装の頑張りポイントでした.
where句が複数の式の組み合わせのケースにも対応しています.
(今思えばnot演算子への対応を忘れてました...)

:::

::: {.column width="70%"}

```kotlin:CandidateFilterByQuery.kt
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

class CandidateFilterByQuery {
    fun filter(sqlQuery: String, candidates: List<Candidate>): List<Candidate> {
        val statement = CCJSqlParserUtil.parse(sqlQuery)
        val select = statement as? Select
        val selectBody = select?.selectBody

        val whereClauseExpression = extractWhereClause(selectBody)
        if (whereClauseExpression == null) {
            println("This query doesn't include Comparison Operator. so return pure candidates.")
            return candidates
        }

        println("This query include Comparison Operator. so conduct candidates filtering.")
        return candidates.filter { isValidCandidateByExpression(it, whereClauseExpression) }
    }

    private fun extractWhereClause(selectBody: SelectBody?): Expression? {
        if (selectBody !is PlainSelect) {
            return null
        }
        return selectBody.where
    }

    private fun isValidCandidateByExpression(candidate: Candidate, whereClause: Expression): Boolean {
        return when (whereClause) {
            is AndExpression -> filterCandidateByAndExpression(candidate, whereClause)
            is OrExpression -> filterCandidateByOrExpression(candidate, whereClause)
            is XorExpression -> filterCandidateByXorExpression(candidate, whereClause)
            else -> filterCandidateBySingleExpression(candidate, whereClause)
        }
    }

    private fun filterCandidateByAndExpression(candidate: Candidate, andExpression: AndExpression): Boolean {
        val isValidLeft = isValidCandidateByExpression(candidate, andExpression.leftExpression)
        val isValidRight = isValidCandidateByExpression(candidate, andExpression.rightExpression)
        return isValidLeft and isValidRight
    }

    private fun filterCandidateByOrExpression(candidate: Candidate, orExpression: OrExpression): Boolean {
        val isValidLeft = isValidCandidateByExpression(candidate, orExpression.leftExpression)
        val isValidRight = isValidCandidateByExpression(candidate, orExpression.rightExpression)
        return isValidLeft or isValidRight
    }

    private fun filterCandidateByXorExpression(candidate: Candidate, xorExpression: XorExpression): Boolean {
        val isValidLeft = isValidCandidateByExpression(candidate, xorExpression.leftExpression)
        val isValidRight = isValidCandidateByExpression(candidate, xorExpression.rightExpression)
        return isValidLeft xor isValidRight
    }

    private fun filterCandidateBySingleExpression(candidate: Candidate, singleExpression: Expression): Boolean {
        if (singleExpression !is ComparisonOperator) {
            return true
        }
        // ここにカラム名や演算子に基づいたフィルタリング処理を実装する
        val column = singleExpression.leftExpression.toString()
        val value = singleExpression.rightExpression.toString().replace("'", "") // 文字列に''が含まれてるので取り除く.

        when (singleExpression) {
            is EqualsTo -> return candidate.getProperty(column) == value

            is GreaterThanEquals -> {
                val property = candidate.getProperty(column)
                if (property !is Double) return false
                return property >= value.toDouble()
            }

            is MinorThanEquals -> {
                val property = candidate.getProperty(column)
                if (property !is Double) return false
                return property <= value.toDouble()
            }
        }
        return true
    }
}
```

:::

::::

# 妄想の問題設定でしたが、とりあえず単体テストが通る様になったのでヨシ！！

## 終わりに...

- **推薦システム × kotlin × LLM(OpenAI API)** をテーマに、ユーザとの対話で推薦結果を変化させる**Interactive Recommender**をkotlinで実装を試みました!
  - 具体的には、「ユーザの自然言語を受け取る -> SQLクエリに変換 -> 推薦記事候補をフィルタリングする」処理をテスト・実装してみた.
- 得られた知見・感想:
  - 最近読んでる"単体テストの考え方/使い方"を参考にテストを書いてみたが、"観察可能な振る舞い"のみをテストする事を意識できた.
  - kotlinはpublicなmethod(観察可能な振る舞い)とprivateなmethod(実装の詳細)を明示的に定義できて嬉しいな...(Pythonが特殊なのかな)

## 参考資料

- 1. [推薦システム実践入門](https://www.oreilly.co.jp/books/9784873119663/)
- 2. 「推薦システムに力を入れている」で私の中で有名なWantedlyさんのData Scientistの方のLT資料: [LLMを活用した推薦システムの改善:課題と初期導入のアプローチ](https://speakerdeck.com/zerebom/llmwohuo-yong-sitatui-jian-sisutemunogai-shan-ke-ti-tochu-qi-dao-ru-noapuroti)
