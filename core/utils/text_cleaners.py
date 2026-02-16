def collapse_spaces(text):
    """
    Standardizes text by collapsing internal multi-spaces 
    and stripping leading/trailing whitespace.
    """
    if text and isinstance(text, str):
        return " ".join(text.split())
    return text
