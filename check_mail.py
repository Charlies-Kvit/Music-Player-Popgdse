from validate_email import validate_email

def check(mail):
    is_valid = validate_email(mail)
    return is_valid