def check_form_data(**kwargs) -> str | None:
    for kwarg in kwargs:
        if not kwargs[kwarg]:
            return f"Field {kwarg} is required."
    return None
