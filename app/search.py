from flask import current_app


def add_to_index(index, model):
    if not current_app.elasticsearch:
        return
    pyload = {}
    for field in model.__searchable__:
        pyload[field] = getattr(model, field)
    current_app.elasticsearch.index(index=index, id=model.id, body=pyload)

def remove_from_index(index, model):
    if not current_app.elasticsearch:
        return
    current_app.elasticsearch.delete(index=index, id=model.id)

def query_index(index, query, page, per_page):
    if not current_app.elasticsearch:
        return [], 0
    
    elastci_query = {'multi_match': {'query': query, 'fields': ['*']}}
    search = current_app.elasticsearch.search(index=index,
                                              body={'query': elastci_query,
                                                    'from': (page - 1) * per_page,
                                                    'size': per_page})

    ids = [int(hit['_id']) for hit in search['hits']['hits']]
    return ids, search['hits']['total']['value']