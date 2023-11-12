from pywikibot.data import api
import pywikibot

from .result import Image, WDEntry
from .util import uppercase_first, pretty_print


IMAGE_PROPS = [
    'P18', # image
    'P14', # traffic sign
    'P41',
    'P94',
    'P158', # seal image
    'P242',
    'P367', # astronomic symbol image
    'P1943',
    'P2716', # collage image
    'P5775', # image of interior
    'P8592', # aerial view
    'P8972', # icon
]



def search_entities(site, search_title, language):
     params = {
         'action' :'wbsearchentities' ,
         'format' : 'json' ,
         'language' : language,
         'type' : 'item',
         'search': search_title,
         'uselang': language
     }

     request = api.Request(site=site, parameters=params)
     return request.submit()


def get_entities(site, wdItem):
     params = {
         'action' :'wbgetentities' ,
         'format' : 'json' ,
         'ids': wdItem,
     }

     request = api.Request(site=site, parameters=params)
     return request.submit()


def get_images_for_entry(site, wdItem):
     params = {
         'action' :'wbgetclaims' ,
         'format' : 'json' ,
         'entity': wdItem,
     }

     request = api.Request(site=site, parameters=params)

     return request.submit()


def get_image_infos(site, wdItem):
    params = {
        'action' : 'query',
        'prop': 'imageinfo|info',
        'inprop': 'url',
        'iiprop': 'url|size|mime',
        'format' : 'json' ,
        'titles': wdItem,
     }

    request = api.Request(site=site, parameters=params)

    return request.submit()


# Login to wikidata
wikidata = pywikibot.Site("wikidata", "wikidata")
commons = pywikibot.Site("commons", "commons")

def get_images_for_search(search_string, language):
    images = []

    wikidata_entries = search_entities(wikidata, search_string, language)

    for wdEntry in wikidata_entries["search"]:
        pretty_print(wdEntry)
        aliases = ", ".join(wdEntry['aliases']) \
            if 'aliases' in wdEntry else ""

        label = wdEntry['display']['label']['value']
        descr = wdEntry['display']['description']['value'] \
            if 'description' in wdEntry['display'] else None

        text =  label + (f" ({aliases})" if aliases != "" else "")

        if wdEntry['match']['language'] != language:
            continue

        match = wdEntry['match']['text']

        if match != search_string and match != uppercase_first(search_string):
            continue

        print(text)

        wdentry = WDEntry(wdEntry["id"], label, descr, text)

        image_claims = get_images_for_entry(wikidata, wdEntry["id"])

        for prop in IMAGE_PROPS:
            if prop not in image_claims['claims']:
                continue

            for image_entry in image_claims['claims'][prop]:
                name = image_entry['mainsnak']['datavalue']['value']
                commons_entry = 'File:' + name
                print("Result name:", commons_entry)
                image_infos = get_image_infos(commons, commons_entry)
                pages = image_infos['query']['pages']
                for key in pages.keys():
                    for iminfo in pages[key]['imageinfo']:
                        images.append(
                            Image(
                                name = name,
                                url = iminfo['url'],
                                caption = uppercase_first(match),
                                wd_entry = wdentry,
                            )
                        )

    return images
