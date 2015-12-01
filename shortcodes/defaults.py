from mezzanine.conf import register_setting

register_setting(
    name='RICHTEXT_ALLOWED_ATTRIBUTES',
    append=True,
    default=('data-name', 'data-pk'),
)

register_setting(
    name='RICHTEXT_FILTERS',
    append=True,
    default=('shortcodes.richtext_filters',),
)
