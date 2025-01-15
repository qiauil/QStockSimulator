from baostock.data.resultset import ResultData

def bs_check_error(result: ResultData):
    if result.error_code != "0":
        raise RuntimeError(
            "error_code: " + result.error_code + ", error_msg: " + result.error_msg
        )
    return result