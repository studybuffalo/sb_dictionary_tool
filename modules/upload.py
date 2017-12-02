import logging

from dictionary.models import (
    WordPending, Language, DictionaryType, DictionaryClass
)


# Setup logging
log = logging.getLogger(__name__)


def upload_words(word_list):
    for lang, dictionary_types in word_list.items():
        language_model = Language.objects.get(language=lang)

        for dict_type, dictionary_classes in dictionary_types.items():
            dict_type_model = DictionaryType.objects.get(
                dictionary_name=dict_type
            )

            for dict_class, words in dictionary_classes.items():
                dict_class_model = DictionaryClass.objects.get(
                    class_name=dict_class
                )

                for dict_word in words:
                    word_model = WordPending(
                        language=language_model,
                        dictionary_type=dict_type_model,
                        dictionary_class=dict_class_model,
                        original_words=dict_word["original_string"],
                        word=dict_word["word"],
                    )
                    try:
                        word_model.save()
                    except Exception:
                        log.warn(
                            (
                                "Unable to save word (Language = {}, "
                                "DictionaryType = {}, DictionaryClass = {} "
                                "Original String = {} Word = {})"
                            ).format(
                                lang, dict_type, dict_class, 
                                dict_word["original_string"], dict_word["word"]
                            ),
                            exc_info=True
                        )