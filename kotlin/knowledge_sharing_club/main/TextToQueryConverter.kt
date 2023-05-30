@file:Suppress("PLUGIN_IS_NOT_ENABLED")

import com.fasterxml.jackson.annotation.JsonIgnoreProperties
import kotlinx.serialization.Serializable
import kotlinx.serialization.decodeFromString
import kotlinx.serialization.json.Json
import okhttp3.OkHttpClient
import okhttp3.Request
import okhttp3.MediaType.Companion.toMediaType
import okhttp3.RequestBody.Companion.toRequestBody
import okhttp3.Response
import okhttp3.ResponseBody


@Serializable
private data class ChatCompletionResponse(
    val id: String,
    val model: String,
    val usage: Map<String, Int>,
    val choices: List<Choice>,
    val created: Int
)

@Serializable
@JsonIgnoreProperties(ignoreUnknown = true)
private data class Choice(
    val message: Message, val finish_reason: String, val index: Int
)

@Serializable
@JsonIgnoreProperties(ignoreUnknown = true)
private data class Message(
    val role: String, val content: String
)

class TextToQueryConverter {

    private val env: MutableMap<String, String> = System.getenv()
    private val apiKey = env["OPENAI_API_KEY"] ?: "empty"
    private val API_ENDPOINT = "https://api.openai.com/v1/chat/completions"
    private val PROMNT_TEMPLATE = """
        あなたの目的は、[ユーザからのコメント]を受け取って、itemsテーブルからユーザが求めるnewsレコードを取得できるようなSQLクエリを作る事です.
        itemsテーブルの各カラムの定義は以下に示します:
        - category(String): It is the category of the news article. unique values are [business, finance, career, eduacition, technology, industry]
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
        val requestBodyString = this.REQUEST_BODY_TEMPLATE.replace("{prompt}", prompt)

        val response = requestToOpenaiApi(requestBodyString)

        return extractAnswer(response.body)
    }

    private fun preparePrompt(userChat: String): String {
        val prompt = this.PROMNT_TEMPLATE.replace("{userChat}", userChat)
        return prompt.replace("[\n\r]".toRegex(), "")
    }

    private fun requestToOpenaiApi(requestBodyString: String): Response {
        val client = OkHttpClient()
        val jsonMediaType = "application/json".toMediaType()

        val requestBody = requestBodyString.toRequestBody(jsonMediaType)
        println(requestBody)
        val request = Request.Builder().url(this.API_ENDPOINT).header("Content-Type", "application/json")
            .header("Authorization", "Bearer $apiKey").post(requestBody).build()

        return client.newCall(request).execute()
    }

    private fun extractAnswer(responseBody: ResponseBody?): String? {
        val BodyString = responseBody?.string() ?: ""
        val json = Json { ignoreUnknownKeys = true }
        val parsedJson = json.decodeFromString<ChatCompletionResponse>(BodyString)
        return parsedJson.choices.firstOrNull()?.message?.content
    }
}


