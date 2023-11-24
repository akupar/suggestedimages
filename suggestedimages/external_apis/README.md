# External APIs

External services to query words.

These provide additional synonyms for words.

The way it works is following. The service must have it's own property (here <service_property>) in Wikidata.

1. Send the search query to the service.
2. The service returns local id (*id*) for the item in the service.
3. Search Wikidata to see if there is an item with *service_property* with the value *id*.
4. Return images for the Wikidata item as usual.

To add a new external service add a handler implementing the Base class and and add the handler to the file *language_api_mapping.py* for the appropriate language(s).
