import logging

from dictionary.models import WordPending, DictionaryType, Language


# Setup logging
log = logging.getLogger(__name__)


def upload_words(word_list):
    for lang, dictionary_types in word_list.items():
        language_model = Language.objects.get(id=lang)

        for dict_type, words in dictionary_types.items():
            dictionary_model = DictionaryType.objects.get(id=dict_type)

            for word in words:
                word_model = WordPending(
                    language=language_model,
                    dictionary_type=dictionary_model,
                    word=word,
                )
                try:
                    word_model.save()
                except Exception:
                    log.warn(
                        (
                            "Unable to save word (Language = {}, "
                            "Dictionary_type = {}, Word = {})"
                        ).format(lang, dict_type, word),
                        exc_info=True
                    )