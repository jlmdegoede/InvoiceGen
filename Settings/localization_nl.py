TEXT_STRINGS = {
    'SETTINGS_SAVED': 'Instellingen opgeslagen',
    'DELETE_INVOICE_FAILED': 'Verwijderen factuur mislukt',
    'DELETE_INVOICE_SUCCESS': 'Verwijderen factuur gelukt',
    'INVOICE_CHANGED': 'Factuur gewijzigd',
    'INVALID_FORM': 'Ongeldig formulier',
    'INVOICE_NOT_FOUND': 'Factuur niet gevonden',
    'INVOICE_CREATED': 'Factuur aangemaakt',
    'USER_DELETED': 'Gebruiker succesvol verwijderd',
    'USER_DELETE_FIRST': 'Je kunt de eerste gebruiker niet verwijderen',
    'NEW_USER_MAIL_SUBJECT': 'Je nieuwe InvoiceGen-account',
    'NEW_USER_MAIL_CONTENTS': 'Beste [USER],\n\nEr is een nieuwe gebruikersaccount voor je aangemaakt op [WEBSITE]. Je kunt inloggen met je e-mailadres en het volgende wachtwoord:\n\n[PASSWORD]\n\nMet vriendelijke groet,\nHet InvoiceGen-team'
}


def get_localized_text(key, dict={}):
    contents = TEXT_STRINGS[key]
    for key, value in dict.items():
        contents = contents.replace(key, value)
    return contents
