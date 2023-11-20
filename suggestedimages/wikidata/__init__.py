from ..locales import Locale
from ..util import StrInLanguage
from .result import Result, CommonsResult, WDEntry, NoImage
from . import api


def get_images_for_word(searched: StrInLanguage, locale: Locale) -> list[tuple[Result, WDEntry]]:
    result_tuples = api.get_images_for_word(searched, locale)

    # Get ranking for results to sort them so that the best results come first.
    ranks = rank_search_results(result_tuples, searched)

    return sorted(
        result_tuples,
        key = lambda pair: ranks[pair[1].id],
        reverse = True,
    )



def rank_search_results(results: list[tuple[Result, WDEntry]], searched: StrInLanguage) -> dict[str, tuple[bool, bool, bool]]:
    entry_ranks = {}

    # Since the results are sorted by the wikidata entry and there are multiple results for each entry,
    # there is one ranking for each entry. We update the same entry for each image in that entry.
    for result_info, entry_info in results:
        if entry_info.id not in entry_ranks:
            entry_ranks[entry_info.id] = (
                False, # Result matches exactly
                True,  # There is at least one image, initalized to True, because there is a NoImages item if no images were found.
                False  # There is a gallery or a category
            )

        exact_case_match = (entry_info.label == searched or searched in entry_info.aliases)
        no_images = (result_info == NoImage)
        gallery_found = (isinstance(result_info, CommonsResult))

        prev_rank = entry_ranks[entry_info.id]
        entry_ranks[entry_info.id] = (
            prev_rank[0] or exact_case_match,
            prev_rank[1] and not no_images,
            prev_rank[2] or gallery_found
        )

    return entry_ranks


if __name__ == "__main__":

    print(get_images_for_word('jänis', 'fi'))
