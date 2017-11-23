import logging

from dictionary.models import Word, WordPending, ExcludedWord


# Setup logging
log = logging.getLogger(__name__)


def extract_new_words(full_word_list):
    """Takes the set of words and collects ones to upload"""
    new_word_list = {}

    for lang, dictionary_types in full_word_list.items():
        # Setup the new word list with the language
        try:
            new_word_list[lang]
        except (KeyError, IndexError):
            new_word_list[lang] = {}

        for dict_type, words in dictionary_types.items():
            # Setup the new word list with the dictionary type 
            try:
                new_word_list[lang][dict_type]
            except (KeyError, IndexError):
                new_word_list[lang][dict_type] = set()

            # Cycle through each word
            for word in words:
                unique = True

                # Check the Word model
                if Word.objects.filter(
                    language=lang, dictionary_type=dict_type, word=word
                ).exists():
                    unique = False

                # Check the WordPending model
                if WordPending.objects.filter(
                    language=lang, dictionary_type=dict_type, word=word
                ).exists():
                    unique = False

                # Check the ExcludedWord model
                if ExcludedWord.objects.filter(
                    language=lang, dictionary_type=dict_type, word=word
                ).exists():
                    unique = False

                if unique:
                    new_word_list[lang][dict_type].add(word)

    return new_word_list
