import logging

from dictionary.models import (
    Language, DictionaryType, DictionaryClass,
    Word, WordPending, ExcludedWord
)


# Setup logging
log = logging.getLogger(__name__)


def extract_new_words(full_word_list):
    """Takes the set of words and collects ones to upload"""
    new_word_list = {}

    for lang, dictionary_types in full_word_list.items():
        log.debug("Collecting unique {} words".format(lang))

        # Setup the new word list with the language
        try:
            new_word_list[lang]
        except (KeyError, IndexError):
            new_word_list[lang] = {}

        # Get the language model entry from Django
        lang_model = Language.objects.get(language=lang)

        for dict_type, dictionary_classes in dictionary_types.items():
            log.debug("Collecting unique {} words".format(dict_type))

            # Setup the new word list with the dictionary type 
            try:
                new_word_list[lang][dict_type]
            except (KeyError, IndexError):
                new_word_list[lang][dict_type] = {}

            # Get the DictionaryType model entry
            dict_type_model = DictionaryType.objects.get(
                dictionary_name=dict_type
            )

            for dict_class, words in dictionary_classes.items():
                log.debug("Collecting unique {} words".format(dict_class))

                # Setup the new word list with the dictonary class
                try:
                    new_word_list[lang][dict_type][dict_class]
                except (KeyError, IndexError):
                    new_word_list[lang][dict_type][dict_class] = []
                    
                # Get the DictionaryClass model entry
                dict_class_model = DictionaryClass.objects.get(
                    class_name=dict_class
                )

                # Cycle through each word
                for word_dict in words["word_list"]:
                    unique = True

                    word = word_dict["word"]
                    word_lower_case = "{}{}".format(word[:1].lower(), word[1:])
                    log.debug("Checking if {} is unique".format(word))

                    # Check the Word model (regular word)
                    if Word.objects.filter(
                        language=lang_model,
                        dictionary_type=dict_type_model, 
                        dictionary_class=dict_class_model, 
                        word=word
                    ).exists():
                        unique = False

                    # Check the Word model (first letter lowercase)
                    if Word.objects.filter(
                        language=lang_model,
                        dictionary_type=dict_type_model, 
                        dictionary_class=dict_class_model, 
                        word=word_lower_case
                    ).exists():
                        unique = False

                    # Check the WordPending model
                    if WordPending.objects.filter(
                        language=lang_model,
                        dictionary_type=dict_type_model, 
                        dictionary_class=dict_class_model, 
                        word=word
                    ).exists():
                        unique = False
                    
                    # Check the WordPending model (first letter lowercase)
                    if WordPending.objects.filter(
                        language=lang_model,
                        dictionary_type=dict_type_model, 
                        dictionary_class=dict_class_model, 
                        word=word_lower_case
                    ).exists():
                        unique = False

                    # Check the ExcludedWord model
                    if ExcludedWord.objects.filter(
                        language=lang_model,
                        dictionary_type=dict_type_model, 
                        dictionary_class=dict_class_model, 
                        word=word
                    ).exists():
                        unique = False
                        
                    # Check the ExcludedWord model (first letter lowercase)
                    if ExcludedWord.objects.filter(
                        language=lang_model,
                        dictionary_type=dict_type_model, 
                        dictionary_class=dict_class_model, 
                        word=word_lower_case
                    ).exists():
                        unique = False

                    if unique:
                        new_word_list[lang][dict_type][dict_class].append(word_dict)
                    
    return new_word_list
