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

class ItemFilter() {
    fun filterByQuery(sqlQuery: String, items: List<Item>): List<Item> {
        val statement = CCJSqlParserUtil.parse(sqlQuery)
        val select = statement as? Select
        val selectBody = select?.selectBody

        val whereClauseExpression = extractWhereClause(selectBody)
        if (whereClauseExpression == null) {
            println("This query doesn't include Comparison Operator. so return pure items.")
            return items // sqlQueryにwhere句が含まれていない場合はそのまま返す.
        }
        println("This query include Comparison Operator. so conduct items filtering.")
        return items.filter { isValidByExpression(it, whereClauseExpression) }
    }

    private fun isValidByExpression(item: Item, whereClause: Expression): Boolean {
        // あるitem情報とwhereClauseを受け取って、booleanを返すfunciton
        return when (whereClause) {
            is AndExpression -> filterItemByAndExpression(item, whereClause)
            is OrExpression -> filterItemByOrExpression(item, whereClause)
            is XorExpression -> filterItemByXorExpression(item, whereClause)
            else -> filterItemBySingleExpression(item, whereClause)
        }
    }

    private fun filterItemByAndExpression(item: Item, andExpression: AndExpression): Boolean {
        val isValidLeft = isValidByExpression(item, andExpression.leftExpression)
        val isValidRight = isValidByExpression(item, andExpression.rightExpression)
        return isValidLeft and isValidRight
    }

    private fun filterItemByOrExpression(item: Item, orExpression: OrExpression): Boolean {
        val isValidLeft = isValidByExpression(item, orExpression.leftExpression)
        val isValidRight = isValidByExpression(item, orExpression.rightExpression)
        return isValidLeft or isValidRight
    }

    private fun filterItemByXorExpression(item: Item, xorExpression: XorExpression): Boolean {
        val isValidLeft = isValidByExpression(item, xorExpression.leftExpression)
        val isValidRight = isValidByExpression(item, xorExpression.rightExpression)
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