def sample(text: str):
    msg=text.lower()
    if msg in ("hi","hello",):
        return "Hey"
    if msg in ("bye"):
        return "Bye!"
    return "Try Again."