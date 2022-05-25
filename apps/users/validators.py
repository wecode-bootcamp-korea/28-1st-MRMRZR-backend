import re


def validate_email(email):
    # 조건 : 이메일 시작은 문자로 시작 + 문자, 숫자, 특수문자 + @ + _와 문자 및 숫자 + . + 문자 및 숫자 + (필요시 . + 문자 및 숫자)
    regex_email = "^[a-zA-Z]+[\w!#$%&'*+-/=?^_`(){|}~]+@[\w]+\.[a-zA-Z0-9-]+[.]*[a-zA-Z0-9]+$"
    return re.match(regex_email, email)

def validate_password(password):
    # 조건 : 최소 8자, 1개 이상의 숫자, 특수문자, 대문자, 소문자 사용 필수 (개행 불가능)
    regex_password = "(?=^.{8,}$)((?=.*\d)|(?=.*\W+))(?![.\n])(?=.*[A-Z])(?=.*[a-z]).*$"
    return re.match(regex_password, password)
