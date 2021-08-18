
import laspy

err_obj = {"FETCH_JSON_FILE_NOT_FOUND": "fetch json file not found"}


def getErrorMsgs(err_code: str) -> str:
    return err_obj[str]


def getErrorObj() -> dict:
    return err_obj
