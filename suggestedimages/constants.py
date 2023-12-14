#NO_IMAGE_THUMB = 'https://upload.wikimedia.org/wikipedia/commons/thumb/4/41/Noimage.svg/320px-Noimage.svg.png'
NO_IMAGE_THUMB = '/static/Noimages.svg'

NUM_COLORS = 12
MORE_IMAGES_CACHE_TIME_IN_SECONDS = 60 * 60 * 24

# The props that are looked for images
# https://www.wikidata.org/wiki/Property:P18 related property (P1659)
IMAGE_PROPS = [
    ("P18", None),
    ("P14", "traffic sign"),
    ("P41", "flag image"),
    ("P94", "coat of arms image"),
    ("P109", "signature"),
    ("P154", "logo image"),
    ("P158", "seal image"),
    ("P242", "locator map image"),
    ("P367", "astronomic symbol image"),
    #("P407", "language of work or name"),
    ("P948", "page banner"),
    ("P996", "document file on Wikimedia Commons"),
    ("P1442", "image of grave"),
    ("P1543", "monogram"),
    ("P1621", "detail map"),
    ("P1766", "place name sign"),
    ("P1801", "plaque image"),
    ("P1943", "location map"),
    ("P1944", "relief location map"),
    ("P2096", "media legend"),
    ("P2713", "sectional view"),
    ("P2716", "collage image"),
    ("P2910", "icon"),
    ("P3311", "image of design plans"),
    ("P3383", "film poster"),
    ("P3451", "nighttime view"),
    ("P4291", "panoramic view"),
    ("P4640", "photosphere image"),
    ("P5137", "item for this sense"),
    ("P5252", "winter view"),
    ("P5775", "image of interior"),
    ("P6500", "non-free artwork image URL"),
    ("P6802", "related image"),
    ("P7407", "name (image)"),
    ("P7415", "code (image)"),
    ("P7417", "image of backside"),
    ("P7418", "image of frontside"),
    ("P8517", "view"),
    ("P8592", "aerial view"),
    ("P8667", "twin town sign"),
    ("P10093", "image with color chart"),
    ("P10253", "reference image"),
    ("P10696", "image set"),
    ("P11101", "model image"),
]
