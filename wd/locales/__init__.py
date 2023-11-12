import importlib

# Source: https://meta.wikimedia.org/wiki/Wiktionary, retrieved 2023-11-12
language_of_wiktionary = {
    'en': 'en', # English
    'fr': 'fr', # French
    'mg': 'mg', # Malagasy
    'zh': 'zh', # Chinese
    'el': 'el', # Greek
    'ru': 'ru', # Russian
    'de': 'de', # German
    'ku': 'ku', # Kurdish
    'es': 'es', # Spanish
    'sh': 'sh', # Serbo-Croatian
    'sv': 'sv', # Swedish
    'nl': 'nl', # Dutch
    'pl': 'pl', # Polish
    'lt': 'lt', # Lithuanian
    'ca': 'ca', # Catalan
    'it': 'it', # Italian
    'hu': 'hu', # Hungarian
    'fi': 'fi', # Finnish
    'pt': 'pt', # Portuguese
    'ta': 'ta', # Tamil
    'tr': 'tr', # Turkish
    'ja': 'ja', # Japanese
    'io': 'io', # Ido
    'hy': 'hy', # Armenian
    'ko': 'ko', # Korean
    'kn': 'kn', # Kannada
    'vi': 'vi', # Vietnamese
    'sr': 'sr', # Serbian
    'th': 'th', # Thai
    'hi': 'hi', # Hindi
    'ro': 'ro', # Romanian
    'id': 'id', # Indonesian
    'no': 'no', # Norwegian
    'et': 'et', # Estonian
    'skr': 'skr', # Saraiki
    'cs': 'cs', # Czech
    'ml': 'ml', # Malayalam
    'my': 'my', # Burmese
    'uz': 'uz', # Uzbek
    'li': 'li', # Limburgish
    'eo': 'eo', # Esperanto
    'or': 'or', # Odia
    'te': 'te', # Telugu
    'fa': 'fa', # Persian
    'gl': 'gl', # Galician
    'sg': 'sg', # Sango
    'oc': 'oc', # Occitan
    'ar': 'ar', # Arabic
    'jv': 'jv', # Javanese
    'is': 'is', # Icelandic
    'az': 'az', # Azerbaijani
    'uk': 'uk', # Ukrainian
    'ast': 'ast', # Asturian
    'eu': 'eu', # Basque
    'br': 'br', # Breton
    'bn': 'bn', # Bangla
    'mnw': 'mnw', # Mon
    'da': 'da', # Danish
    'simple': 'en', # Simple English
    'lo': 'lo', # Lao
    'la': 'la', # Latin
    'shn': 'shn', # Shan
    'hr': 'hr', # Croatian
    'sk': 'sk', # Slovak
    'fj': 'fj', # Fijian
    'wa': 'wa', # Walloon
    'ky': 'ky', # Kyrgyz
    'lmo': 'lmo', # Lombard
    'bg': 'bg', # Bulgarian
    'ur': 'ur', # Urdu
    'cy': 'cy', # Welsh
    'ps': 'ps', # Pashto
    'tg': 'tg', # Tajik
    'kbd': 'kbd', # Kabardian
    'he': 'he', # Hebrew
    'vo': 'vo', # Volapük
    'om': 'om', # Oromo
    'sl': 'sl', # Slovenian
    'af': 'af', # Afrikaans
    'nan': 'nan', # Min Nan Chinese
    'ms': 'ms', # Malay
    'scn': 'scn', # Sicilian
    'tl': 'tl', # Tagalog
    'pa': 'pa', # Punjabi
    'fy': 'fy', # Western Frisian
    'sw': 'sw', # Swahili
    'kk': 'kk', # Kazakh
    'ka': 'ka', # Georgian
    'nn': 'nn', # Norwegian Nynorsk
    'min': 'min', # Minangkabau
    'lv': 'lv', # Latvian
    'nds': 'nds', # Low German
    'gor': 'gor', # Gorontalo
    'sq': 'sq', # Albanian
    'lb': 'lb', # Luxembourgish
    'bs': 'bs', # Bosnian
    'co': 'co', # Corsican
    'mn': 'mn', # Mongolian
    'pnb': 'pnb', # Western Punjabi
    'nah': 'nah', # Nāhuatl
    'yue': 'yue', # Cantonese
    'ckb': 'ckb', # Central Kurdish
    'sa': 'sa', # Sanskrit
    'diq': 'diq', # Zazaki
    'km': 'km', # Khmer
    'be': 'be', # Belarusian
    'vec': 'vec', # Venetian
    'nia': 'nia', # Nias
    'tk': 'tk', # Turkmen
    'mk': 'mk', # Macedonian
    'sm': 'sm', # Samoan
    'hsb': 'hsb', # Upper Sorbian
    'ks': 'ks', # Kashmiri
    'shy': 'shy', # Shawiya
    'bcl': 'bcl', # Central Bikol
    'su': 'su', # Sundanese
    'ga': 'ga', # Irish
    'btm': 'btm', # Batak Mandailing
    'gd': 'gd', # Scottish Gaelic
    'an': 'an', # Aragonese
    'gom': 'gom', # Goan Konkani
    'mr': 'mr', # Marathi
    'ha': 'ha', # Hausa
    'wo': 'wo', # Wolof
    'mni': 'mni', # Manipuri
    'ia': 'ia', # Interlingua
    'bjn': 'bjn', # Banjar
    'ang': 'ang', # Old English
    'mt': 'mt', # Maltese
    'tt': 'tt', # Tatar
    'sd': 'sd', # Sindhi
    'blk': 'blk', # Pa'O
    'fo': 'fo', # Faroese
    'so': 'so', # Somali
    'si': 'si', # Sinhala
    'gn': 'gn', # Guarani
    'ie': 'ie', # Interlingue
    'mi': 'mi', # Māori
    'csb': 'csb', # Kashubian
    'ug': 'ug', # Uyghur
    'guw': 'guw', # Gun
    'st': 'st', # Southern Sotho
    'hif': 'hif', # Fiji Hindi
    'jbo': 'jbo', # Lojban
    'roa-rup': 'rup', # Aromanian
    'kl': 'kl', # Kalaallisut
    'zu': 'zu', # Zulu
    'ay': 'ay', # Aymara
    'ln': 'ln', # Lingala
    'yi': 'yi', # Yiddish
    'gu': 'gu', # Gujarati
    'kcg': 'kcg', # Tyap
    'na': 'na', # Nauru
    'gv': 'gv', # Manx
    'kw': 'kw', # Cornish
    'tpi': 'tpi', # Tok Pisin
    'am': 'am', # Amharic
    'ne': 'ne', # Nepali
    'rw': 'rw', # Kinyarwanda
    'ts': 'ts', # Tsonga
    'ig': 'ig', # Igbo
    'qu': 'qu', # Quechua
    'ss': 'ss', # Swati
    'iu': 'iu', # Inuktitut
    'chr': 'chr', # Cherokee
    'dv': 'dv', # Divehi
    'ti': 'ti', # Tigrinya
    'tn': 'tn', # Tswana
}


class Locale:
    def __init__(self, wikt):
        try:
            self.language = language_of_wiktionary[wikt]
        except KeyError:
            raise Exception(f'No such wiktionary: {self.wikt}')
        self.wikt = wikt

        try:
            self.module = importlib.import_module(f'wd.locales.{wikt}')
        except ImportError:
            self.module = None

    def __repr__(self):
        return f"Locale({self.wikt}, language={self.language})"

    def __getitem__(self, key):
        if not self.module:
            return key

        return self.module.texts.get(key, key)

    def format_image(self, name, caption):
        if name.startswith('File:'):
            name = name[len('File:'):]
        return f"[[{self['File']}:{name}|{self['thumb']}|{caption}]]"



DEFAULT_LOCALE = Locale('en')
