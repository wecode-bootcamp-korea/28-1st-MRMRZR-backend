import re

def validate_email(email):
    regex_email = r"^[a-zA-Z]+[\w!#$%&'*+-/=?^_`(){|}~]+@[\w]+\.[a-zA-Z0-9-]+[.]*[a-zA-Z0-9]+$"
    return re.match(regex_email, email)

def validate_password(password):
    regex_password = r'([\w!@#$%^&*(),.?\":{}|<>]+){8}'
    return re.match(regex_password, password)
