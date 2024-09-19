from ninja.responses import Response
from http import HTTPStatus


class ErrorCode:
    UNAUTHORIZED_USER = "unauthorized_user"
    NETWORK_FAILURE = "network_failure"
    SERVER_ERROR = "server_error"
    INVALID_ENTRY = "invalid_entry"
    INCORRECT_EMAIL = "incorrect_email"
    INVALID_OTP = "invalid_otp"
    INVALID_AUTH = "invalid_auth"
    INVALID_TOKEN = "invalid_token"
    INVALID_CREDENTIALS = "invalid_credentials"
    UNVERIFIED_USER = "unverified_user"
    NON_EXISTENT = "non_existent"
    INVALID_OWNER = "invalid_owner"
    INVALID_PAGE = "invalid_page"
    INVALID_VALUE = "invalid_value"
    NOT_ALLOWED = "not_allowed"
    INVALID_DATA_TYPE = "invalid_data_type"


class RequestError(Exception):
    default_detail = "An error occured"

    def __init__(
        self, err_code: str, err_msg: str, status_code: int = 400, data: dict = None
    ) -> None:
        self.status_code = HTTPStatus(status_code)
        self.err_code = err_code
        self.err_msg = err_msg
        self.data = data

        super().__init__()


class NotFoundError(RequestError):
    def __init__(
        self,
        err_msg: str,
        err_code: str = ErrorCode.NON_EXISTENT,
        status_code: int = 404,
        data: dict = None,
    ) -> None:
        super().__init__(err_msg, err_code, status_code, data)


class ValidationErr(RequestError):
    def __init__(
        self,
        field: str,
        message: str,
        err_msg: str = "Invalid Entry",
        err_code: str = ErrorCode.INVALID_ENTRY,
        status_code: int = 422,
    ) -> None:
        data = {field: message}
        super().__init__(err_msg, err_code, status_code, data)


def validation_errors(exc):
    # Get the original 'detail' list of errors
    details = exc.errors
    modified_details = {}
    for error in details:
        field_name = error["loc"][-1]
        err_msg = error["msg"]
        err_type = error["type"]
        if err_type == "value_error.any_str.min_length":
            err_msg = f"{error['ctx']['limit_value']} characters min"
        elif err_type == "value_error.any_str.max_length":
            err_msg = f"{error['ctx']['limit_value']} characters max"
        elif err_type == "value_error.list.max_items":
            err_msg = f"{error['ctx']['limit_value']} items max"
        elif err_type == "value_error.list.min_items":
            err_msg = f"{error['ctx']['limit_value']} item min"
        elif err_type == "type_error.enum":
            allowed_enum_values = ", ".join(
                [value.name for value in error["ctx"]["enum_values"]]
            )
            err_msg = f"Invalid choice! Allowed: {allowed_enum_values}"
        modified_details[f"{field_name}"] = err_msg

    return Response(
        {
            "status": "failure",
            "code": ErrorCode.INVALID_ENTRY,
            "message": "Invalid Entry",
            "data": modified_details,
        },
        status=422,
    )


def request_errors(exc):
    err_dict = {
        "status": "failure",
        "code": exc.err_code,
        "message": exc.err_msg,
    }
    if exc.data:
        err_dict["data"] = exc.data
    return Response(err_dict, status=exc.status_code)
