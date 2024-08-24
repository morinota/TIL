# RDSに結果を書き込むstepを定義


def access_to_rds(
    rds_user: str,
    rds_password: str,
    rds_db: str,
    rds_host: str,
    sql_query: str,
) -> bool:
    import pymysql
    from loguru import logger

    logger.debug("access to rds")

    # RDSに接続
    logger.debug(f"connect to {rds_host=}")
    try:
        connection = pymysql.connect(
            host=rds_host,
            user=rds_user,
            password=rds_password,
            db=rds_db,
            connect_timeout=5,
            port=3306,
        )
    except pymysql.MySQLError as e:
        logger.error(f"ERROR: Unexpected error: Could not connect to MySQL instance.")
        logger.error(e)
        raise

    with connection.cursor() as cursor:
        cursor.execute(sql_query)
        result = cursor.fetchall()
        logger.debug(f"query result: {result}")

    return True
