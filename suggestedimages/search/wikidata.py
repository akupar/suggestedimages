from ..util import StrInLanguage, StrInLanguages
from ..localization import Locale
from .result import WDEntry


def get_entry_description(entry, searched: StrInLanguage, locale: Locale) -> WDEntry:
    label = StrInLanguages(entry.labels).get(searched.language) or locale["[no label]"]
    aliases = StrInLanguages(entry.aliases).get(searched.language)

    translation = None
    if locale.language != searched.language:
        translation = StrInLanguages(entry.labels).get(locale.language)
        if not translation and searched.language != 'en':
            translation = StrInLanguages(entry.labels).get('en')

    description = StrInLanguages(entry.descriptions).get(locale.language, 'en', searched.language)

    tooltip = build_composite_description(label, aliases, translation, description)

    return WDEntry(
        entry.id,
        label,
        aliases or [],
        description,
        tooltip,
        entry.full_url(),
    )

def build_composite_description(label, aliases, translation, description):
    """Combines descriptive texts into one text.
    """
    return spaced((label if label else None),
                  ((f"({', '.join([str(alias) for alias in aliases])})") if aliases else None),
                  ((f"[= {translation}]") if translation else None)) \
                  + ((f": {description}") if description else "")

def spaced(*args):
    return " ".join(str(arg) for arg in args if arg != None)
