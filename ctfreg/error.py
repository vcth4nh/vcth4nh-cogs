from requests.exceptions import JSONDecodeError

class ApiNotFound(Exception):
    pass

class DataNotJson(JSONDecodeError):
    pass