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
}


def get_localized_text(key):
    return TEXT_STRINGS[key]