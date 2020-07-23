class Marker:
    none = lambda x: x
    upper = lambda x: x.upper()
    lower = lambda x: x.lower()
    ellipsis = lambda x: "..."
    censor = lambda x: "***"

    # html tags
    bold = lambda x: f"<b>{x}</b>"
    italic = lambda x: f"<i>{x}</i>"


class Subcorpus:
    class Persons:
        Pushkin = 'JSONeyJkb2NfYXV0aG9yIjogWyLQkC7QoS4g0J_Rg9GI0LrQuNC9Il19'
        Dostoyevsky = 'JSONeyJkb2NfYXV0aG9yIjogWyLQpC7QnC4g0JTQvtGB0YLQvtC10LLRgdC60LjQuSJdfQ%3D%3D'
        TolstoyLN = 'JSONeyJkb2NfYXV0aG9yIjogWyLQmy7QnS4g0KLQvtC70YHRgtC-0LkiXX0%3D'
        Chekhov = 'JSONeyJkb2NfYXV0aG9yIjogWyLQkC7Qny4g0KfQtdGF0L7QsiJdfQ%3D%3D'

    class Parallel:
        # it works sometime
        set_subcorp = lambda lang: f'%28lang%3A"{lang}"+%7C+lang_trans%3A"{lang}"%29'

        English = 'JSONeyJkb2NfbGFuZyI6IFsiZW5nIl0sICJpc19wYXJhX2JvdGhfcGFpcnMiOiBbdHJ1ZV19'
        Armenian = '%28lang%3A"arm"+%7C+lang_trans%3A"arm"%29'
        Bashkir = '%28lang%3A"bash"+%7C+lang_trans%3A"bash"%29'
        Belarusian = '%28lang%3A"bel"+%7C+lang_trans%3A"bel"%29'
        Bulgarian = '%28lang%3A"bul"+%7C+lang_trans%3A"bul"%29'
        Buryatian = '%28lang%3A"bua"+%7C+lang_trans%3A"bua"%29'
        Spanish = '%28lang%3A"esp"+%7C+lang_trans%3A"esp"%29'
        Italian = '%28lang%3A"ita"+%7C+lang_trans%3A"ita"%29'
        # In developing, wait some time...
        # Chinese = '%28lang%3A%22zho%22+%7C+lang_trans%3A%22zho%22%29'
        Latvian = '%28lang%3A"lav"+%7C+lang_trans%3A"lav"%29'
        Lithuanian = '%28lang%3A"lit"+%7C+lang_trans%3A"it"%29'
        German = '%28lang%3A"ger"+%7C+lang_trans%3A"ger"%29'

        Polish = '%28lang%3A"pol"+%7C+lang_trans%3A"pol"%29'
        Ukrainian = '%28lang%3A"ukr"+%7C+lang_trans%3A"ukr"%29'
        French = '%28lang%3A"fra"+%7C+lang_trans%3A"fra"%29'
        Finnish = '%28lang%3A"fin"+%7C+lang_trans%3A"fin"%29'
        Czech = '%28lang%3A"cze"+%7C+lang_trans%3A"cze"%29'
        Swedish = 'mycorp=%28lang%3A"sve"+%7C+lang_trans%3A"sve"%29'
        Estonian = '%28lang%3A"est"+%7C+lang_trans%3A"est"%29'
        Multilingual = ''
        RCinGT = ''
