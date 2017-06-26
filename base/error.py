class Error:
    NOT_FOUND_KEYWORD = 2002
    FAILED_GRAB = 2001
    ERROR_PASSWORD = 2000
    NEED_LOGIN = 1003
    REQUIRE_JSON = 1002
    REQUIRE_PARAM = 1001
    NOT_FOUND_ERROR = 1000
    OK = 0

    ERROR_DICT = [
        (NOT_FOUND_KEYWORD, "不存在的关键词"),
        (FAILED_GRAB, "抓取失败"),
        (ERROR_PASSWORD, "错误的用户名或密码"),

        (NEED_LOGIN, "需要登录"),
        (REQUIRE_JSON, "需要JSON数据"),
        (REQUIRE_PARAM, "缺少参数"),
        (NOT_FOUND_ERROR, "不存在的错误"),
        (OK, "没有错误"),
    ]
