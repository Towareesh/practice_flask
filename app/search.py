from app import fts_engine


def clear_column(df, index: str):
    # df - is data frame pd.DataFrame
    df[index] = ((df[index]
                   .str.replace(r'[^a-zA-Z0-9А-Яа-я]',' ', regex=True)
                   .str.split()
                   .apply(lambda x: ' '.join([i.strip() for i in x]))
                   .str.lower()))
    return df

def query_index(index: list, model, query):

    sqlite_select_query = f"""SELECT id, {index}
                              FROM {model}"""
    db_query = fts_engine.sqlite_query(sqlite_select_query)
    df       = fts_engine.get_data_frame('id', index, db_query=db_query)
    fts_engine.create_virtual_table(df, ['id', index])
    answer   = fts_engine.search_fetchall_query(query, index)
    
    ids   = [int.from_bytes(i[0], "little") for i in answer]
    ranks = [abs(i[-1]) for i in answer]
    return ids, ranks