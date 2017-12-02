import logging
import re

# Setup logging
log = logging.getLogger(__name__)

def retrieve_hc_dpd_words():
    """Extracts all words from the hc_dpd application"""
    from hc_dpd.models import (
        ActiveIngredient, Company, DrugProduct, SubBrand, SubCompanyName, 
        SubIngredient
    )

    # Setup the words dictionary to hold all the retrieved words
    words = {
        "English": {
            "company_names": {
                "disinfectant": {
                    "word_set": set(),
                    "word_list": []
                },
                "human": {
                    "word_set": set(),
                    "word_list": []
                },
                "veterinary": {
                    "word_set": set(),
                    "word_list": []
                },
            },
            "trade_names": {
                "disinfectant": {
                    "word_set": set(),
                    "word_list": []
                },
                "human": {
                    "word_set": set(),
                    "word_list": []
                },
                "veterinary": {
                    "word_set": set(),
                    "word_list": []
                },
            },
            "ingredients": {
                "disinfectant": {
                    "word_set": set(),
                    "word_list": []
                },
                "human": {
                    "word_set": set(),
                    "word_list": []
                },
                "veterinary": {
                    "word_set": set(),
                    "word_list": []
                },
            }
        },
        "French": {
            "company_names": {
                "disinfectant": {
                    "word_set": set(),
                    "word_list": []
                },
                "human": {
                    "word_set": set(),
                    "word_list": []
                },
                "veterinary": {
                    "word_set": set(),
                    "word_list": []
                },
            },
            "trade_names": {
                "disinfectant": {
                    "word_set": set(),
                    "word_list": []
                },
                "human": {
                    "word_set": set(),
                    "word_list": []
                },
                "veterinary": {
                    "word_set": set(),
                    "word_list": []
                },
            },
            "ingredients": {
                "disinfectant": {
                    "word_set": set(),
                    "word_list": []
                },
                "human": {
                    "word_set": set(),
                    "word_list": []
                },
                "veterinary": {
                    "word_set": set(),
                    "word_list": []
                },
            }
        }
    }

    # Extract the trade name words
    log.debug("Retrieving trade names")

    trade_names = SubBrand.objects.all().values_list("substitution", flat=True)
    
    for trade_name in trade_names:
        log.debug("Extracting and process words from '{}'".fromat(trade_name))

        # Get references to any entry this substitution applies to
        drug_products = DrugProduct.objects.filter(
            brand_name=trade_name
        )

        for product in drug_products:
            class_name = product.class_e.lower()
            word_dict = words["English"]["Trade names"][class_name]
            
            word_list = re.findall(r"[\w']+", trade_name)
            
            for word in word_list:
                # Check if this word is already in the set
                if word not in word_dict["word_set"]:
                    # Add word to set
                    word_dict["word_set"].add(word)

                    # Add diciontary to word_list
                    word_dict["word_list"].append({
                        "original_string": trade_name,
                        "word": word,
                    })
                
    # Extract the ingredient words
    log.debug("Retrieving ingredients")

    ingredients = SubIngredient.objects.all().values_list(
        "substitution", flat=True
    )

    for ingredient in ingredients:
        log.debug("Extracting and process words from '{}'".fromat(ingredient))

        # Get references to any entry this substitution applies to
        active_ingredients = ActiveIngredient.objects.filter(
            ingredient=ingredient
        )

        for active_ingredient in active_ingredients:
            # Get the proper class name for this active_ingredient
            try:
                class_name = DrugProduct.objects.get(
                    drug_code=active_ingredient.drug_code
                ).class_e.lower()
            except MultipleObjectsReturned:
                log.warn(
                    "Multiple DrugProducts with same drug code",
                    exc_info=True
                )
                class_name = DrugProduct.objects.filter(
                    drug_code=active_ingredient.drug_code
                )[0].class_e.lower()
            except DoesNotExist:
                class_name = ""

            # Setup reference to word_dictioanry & create word_list
            try:
                word_dict = words["English"]["Ingredients"][class_name]
                word_list = re.findall(r"[\w']+", ingredient)
            except IndexError:
                log.warn(
                    "Invalid class name provided: {}".format(class_name),
                    exc_info=True
                )
            
            # Add each unique word to the dictionary
            for word in word_list:
                # Check if this word is already in the set
                if word not in word_dict["word_set"]:
                    # Add word to set
                    word_dict["word_set"].add(word)

                    # Add diciontary to word_list
                    word_dict["word_list"].append({
                        "original_string": ingredient,
                        "word": word,
                    })
                
    # Extract the company words
    log.debug("Retrieving company names")

    company_names = SubCompanyName.objects.all().values_list(
        "substitution", flat=True
    )

    for name in company_names:
        log.debug("Extracting and process words from '{}'".fromat(name))

        # Get references to any entry this substitution applies to
        companies = Company.objects.filter(
            company_name=name
        )

        for company in companies:
            # Get the proper class name for this active_ingredient
            try:
                class_name = DrugProduct.objects.get(
                    drug_code=company.drug_code
                ).class_e.lower()
            except MultipleObjectsReturned:
                log.warn(
                    "Multiple DrugProducts with same drug code",
                    exc_info=True
                )
                class_name = DrugProduct.objects.filter(
                    drug_code=company.drug_code
                )[0].class_e.lower()
            except DoesNotExist:
                class_name = ""

            # Setup reference to word_dictioanry & create word_list
            try:
                word_dict = words["English"]["Pharmaceutical company names"][class_name]
                word_list = re.findall(r"[\w']+", name)
            except IndexError:
                log.warn(
                    "Invalid class name provided: {}".format(class_name),
                    exc_info=True
                )
            
            # Add each unique word to the dictionary
            for word in word_list:
                # Check if this word is already in the set
                if word not in word_dict["word_set"]:
                    # Add word to set
                    word_dict["word_set"].add(word)

                    # Add diciontary to word_list
                    word_dict["word_list"].append({
                        "original_string": name,
                        "word": word,
                    })

    return words

def retrieve_words(application):
    """Uses the provided application to return a word list"""
    if application.upper() == "HC_DPD":
        log.info("Retrieving HC DPD application words")
        return retrieve_hc_dpd_words()
