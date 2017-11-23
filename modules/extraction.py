from django.apps import apps
import logging
import re

from dictionary.models import MonitoredApplication


# Setup logging
log = logging.getLogger(__name__)


def retrieve_words():
    """Extracts all words from fields listed in Dictionary App"""
    # COLLECT ALL THE DATABASE VALUES
    words = {}

    # Get all the MonitoredApplications
    applications = MonitoredApplication.objects.all()

    for app in applications:
        # Get all the referenced models
        models = app.monitoredmodel_set.all()

        for model in models:
            # Get all the referenced fields
            fields = model.monitoredfield_set.all()

            # Get a model reference
            model_reference = apps.get_model(
                app.application_name, model.model_name
            )

            # Get the values for the monitored fields
            for field in fields:
                field_values = model_reference.objects.values(field.field_name)
                dictionary_type = field.dictionary_type.id
                language = field.language.id

                # Add the dictionary and language as indices to array
                try:
                    words[language]
                except (KeyError, IndexError):
                    words[language] = {}

                try:
                    words[language][dictionary_type]
                except (KeyError, IndexError):
                    words[language][dictionary_type] = set()

                for value in field_values:
                    word_list = re.findall(r"[\w']+", value[field.field_name])

                    words[language][dictionary_type].update(word_list)
                
    return words