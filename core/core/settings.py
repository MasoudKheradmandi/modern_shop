from split_settings.tools import optional, include


include(
    'base.py',
    optional('settings.prod.py'),
    optional('settings.dev.py'),

)
