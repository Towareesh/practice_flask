import translators as ts
from flask_babel import _


def translate_text(text: str,
                   source_language: str, dest_lang: str,
                   access_speed=False, api_provider='bing'):

    if access_speed:
        # Optional. Caching sessions in advance, which can help improve access speed.
        ts.preaccelerate()
    
    try: 
        result = ts.translate_text(text,
                                   translator    = api_provider,
                                   from_language = source_language,
                                   to_language   = dest_lang)
    except:
        result = _('Error: the translation service failed.')
    
    return result