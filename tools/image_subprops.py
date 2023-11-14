import pywikibot
from pywikibot import pagegenerators
from pywikibot.data.sparql import SparqlQuery
from wd.util import pretty_print

site = pywikibot.Site("wikidata", "wikidata")
repo = site.data_repository()

query = '''
SELECT ?value ?valueLabel
WHERE
{
  wd:P18 wdt:P1659 ?value .
  SERVICE wikibase:label { bd:serviceParam wikibase:language "en". }
}
'''

q = SparqlQuery(repo=repo)



print("IMAGE_PROPS = [")

for binding in q.query(query)['results']['bindings']:
    print('    ("', binding['value']['value'].split('/')[-1], '", "', binding['valueLabel']['value'], '"),', sep="")

print("]")
