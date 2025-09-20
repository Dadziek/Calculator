def tokenize(expr: str) -> list[str]:
    tokens = []
    number, word = '', ''
    for ch in expr:
        if ch.isdigit() or ch == '.':
            number += ch
        elif ch.isalpha():
            word += ch
        else:
            if number:
                tokens.append(number)
                number = ''
            if word:
                tokens.append(word)
                word = ''
            if ch in '+-*/^()%!,':
                tokens.append(ch)
    if number:
        tokens.append(number)
    if word:
        tokens.append(word)
    return tokens
