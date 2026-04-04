
class FENPatterns:

    rank             = r"[1-8]"
    file             = r"[a-h]"
    square           = rf"{file}{rank}"
    integer          = r"[0-9]+"
    blank            = r"[\s]+"
    none             = r"[-]"
    
    to_move         = r"[wb]"
    castling_rights = rf"K?Q?k?q?|{none}"
    en_passant      = rf"{square}|{none}"
    row             = r"[PNBRQKpnbrqk1-8]+"
    board           = rf"(?:{row}/)" + r"{7}" + row

    fen  = (rf"^(?P<board>{board})"
            + rf"{blank}(?P<to_move>{to_move})"
            + rf"{blank}(?P<castling_rights>{castling_rights})"
            + rf"{blank}(?P<en_passant>{en_passant})"
            + rf"{blank}(?P<half_moves>{integer})"
            + rf"{blank}(?P<moves>{integer})$")