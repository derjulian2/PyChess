
class PGNPatterns:

    word      = r"[\w]*"
    words     = r"[\w\s]*"
    integer   = r"[0-9]+"
    blank     = r"[\s]+"
    blank_opt = r"[\s]*"
    newline   = r"[\r\n]"
    meta_pair = rf"\[{blank_opt}(?P<key>{word}){blank}\"(?P<value>{words})\"{blank_opt}\]"
    move      = rf"(?P<turn_num>{integer}).{blank}" + r"(?P<move>[NBRQKxa-h1-8()=#+]{2,})"
    comment   = r"\{" + f"({words})" + r"\}"

    # block-parsing in first-pass:
    # determine if document is structured into meta-block and moves-block.
    # match the individual results with .meta_pair and .algebraic_move afterwards.
    meta_block = r"(?:\[[^\[\]]+\][\r\n\s]*)+"
    move_block = rf"(?:{integer}.{blank}" + r"[NBRQKxa-h1-8()=#+]{2,}" + r"[\r\n\s]+)+"  

    pgn        = rf"({meta_block})[\r\n\s]+({move_block})"