import hashlib


def md5(input: str) -> str:
    """
    Calculate md5 hash of input string
    :param input:
    :return:
    """
    return hashlib.md5(input.encode()).hexdigest()


def sha1(input: str) -> str:
    """
    Calculate sha1 hash of input string
    :param input:
    :return:
    """
    return hashlib.sha1(input.encode()).hexdigest()


def sha256(input: str) -> str:
    """
    Calculate sha256 hash of input string
    :param input:
    :return:
    """
    return hashlib.sha256(input.encode()).hexdigest()
