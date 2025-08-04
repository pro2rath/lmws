# lwms/utils/tamil_unicode.py

# A simple dictionary to hold Tamil translations for the UI.
# In a larger app, this would be managed with a proper i18n library.

TAMIL_STRINGS = {
    'title': 'தொழிலாளர் மேலாண்மை அமைப்பு',
    'welcome': 'வருக!',
    'register_worker': 'தொழிலாளரைப் பதிவு செய்யுங்கள்',
    'search_worker': 'தொழிலாளரைத் தேடுங்கள்',
    'daily_availability': 'தினசரி வருகை',
    'privacy_policy': 'தனியுரிமைக் கொள்கை'
}

def get_tamil_string(key):
    """Returns the Tamil string for a given key."""
    return TAMIL_STRINGS.get(key, key)