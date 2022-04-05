import re


def check_form_data(**kwargs) -> str | None:
    for kwarg in kwargs:
        if not kwargs[kwarg]:
            return f"Field {kwarg} is required."
    return None


def check_email(email: str) -> bool:
    regex = r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b"
    return True if re.fullmatch(regex, email) else False
