A [Mezzanine](https://github.com/stephenmcd/mezzanine) package that allows you to add buttons and menus to the richtext editor by simply decorating a python function.

This package aims to fulfill the same needs as Wordpress's shortcodes but with the following advantages:

- Fallback to removing placeholder so if something goes wrong it is not shown to end-users. I've seen shortcode literals accidentally displayed on Wordpress sites too many times, though often due to syntax errors which we avoid by...
- Integration with the richtext editor so users have a seamless experience that doesn't involve learning syntax. CMS users shouldn't be writing any *code* -- long or short.

A mezzaine-shortcode is just a python function paired with a `ModelForm`. The `ModelForm` allows users to create content to insert into the page, while the function behaves similar to a Django view, with the following substitutions:
- Accepts a `ModelForm` instance as its sole argument rather than an `HttpRequest`.
- Returns a string of html rather than an `HttpResponse`.

Screenshots
===========

![TinyMCE toolbar with custom buttons and menus.](/../screenshots/toolbar.jpeg)

![Dialog after clicking a custom button.](/../screenshots/dialog.jpeg)

![Represenation of inserted shortcode in textbox.](/../screenshots/representation.jpeg)

Compatibility
=============

- Python 3.x only. It wouldn't be too difficult to make this backwards compatible but it currently is not.
- I've only tested with Mezzanine 4.x, but I don't know of any reason it wouldn't work with older versions.

Installation
============

Pip install this package:

```sh
pip install mezzanine-shortcodes
```

Now make the following changes in your project:

*settings.py*

```py
######################
# MEZZANINE SETTINGS #
######################

RICHTEXT_WIDGET_CLASS = 'shortcodes.forms.TinyMceWidget'

# This static file can be anywhere you please but you must define it.
TINYMCE_SETUP_JS = 'js/tinymce_setup.js'

################
# APPLICATIONS #
################

INSTALLED_APPS = (
    ...
    'shortcodes',
)
```

*urls.py*

```py
urlpatterns = [
    ...
    # MEZZANINE-SHORTCODE'S URLS
    # --------------------------
    url("^shortcodes/", include('shortcodes.urls')),
    ...
    # MEZZANINE'S URLS
    # ----------------
    # ADD YOUR OWN URLPATTERNS *ABOVE* THE LINE BELOW.
    # ``mezzanine.urls`` INCLUDES A *CATCH ALL* PATTERN
    # FOR PAGES, SO URLPATTERNS ADDED BELOW ``mezzanine.urls``
    # WILL NEVER BE MATCHED!
]
```

*tinymce_setup.js*

- Add `shortcodes` to `plugins`.
- Add whatever menus or buttons you've created to `toolbar`.
- Add `/static/shortcodes/tinymce/style.css` to `content_css` array.
- Set `valid_elements` to `*[*]` to allow all.
- Add `shortcode` to `contextmenu`.


```js
tinyMCE.init({
  ...
  plugins: [
      "advlist autolink lists link image charmap print preview anchor",
      "searchreplace visualblocks code fullscreen",
      "insertdatetime media table contextmenu paste shortcodes"
  ],
  toolbar: ("insertfile undo redo | styleselect | bold italic | " +
            "alignleft aligncenter alignright alignjustify | " +
            "bullist numlist outdent indent | link image table | " +
            "example_menu example_button | code fullscreen"),
  content_css: [window.__tinymce_css, '/static/shortcodes/tinymce/style.css'],
  valid_elements: "*[*]",
  contextmenu: "shortcode | link image inserttable | cell row column deletetable"
});
```

API Reference
=============

Add your shortcode definitions to a `shortcodes.py` module in any installed app.

*All buttons/menubuttons must have unique names (`__name__`). All `ModelForm`'s must have unique `verbose_name`'s and a `ModelForm` cannot be associated with multiple shortcodes.*

Buttons
-------

Buttons are created with the `button` decorator, which takes the following parameters:

- `modelform` (**required**): Reference to a `ModelForm`.
- `icon` (*optional*): The string path to an image file starting from the static url. *'Free' buttons cannot display both a name and an icon, so `verbose_name` is not shown if this is defined.*
- `tooltip` (*optional*): The string displayed on mouseover.

```py
@shortcodes.button(
    MyModelForm
    icon='path/to/image.png',
    tooltip='Click me.')
def my_button(instance):
    return '<div>Some html string.</div>'
```

### Generic Buttons

In some cases, it may be simpler to instantiate a button with `GenericButton`, which takes the following parameters:

- `name` (**required**): The identifying name that you'll pass into the tinymce toolbar.
- `modelform` (**required**): Reference to a `ModelForm`.
- `template` (**required**): A string template name which will be rendered with the associated model instance's fields in the context.
- *... same kwargs as regular Buttons*

```py
shortcodes.GenericButton('my_button', MyModelForm, 'some_template.html')
```

Menus
-----

Menus are just dropdown collections of buttons. They inherit from `shortcodes.Menu` and have the following optional class attributes:

- `displayname`: The string to display in the toolbar.
- `tooltip`: The string displayed on mouseover.

Menubuttons are registered with the `shortcodes.menubutton` decorator, which takes the same arguments as regular buttons.

```py
class SomeMenu(shortcodes.Menu):
    displayname='Some Menu'
    tooltip='Input your stuff'

    @shortcodes.menubutton(MyModelForm)
    def some_menubutton(instance):
        ...
```

Or with `shortcodes.GenericMenubutton` which behaves identically to regular generic buttons except it's in class scope:

```py
class SomeMenu(shortcodes.Menu):

    shortcodes.GenericMenubutton(
        'some_menubutton', MyModelForm, 'some_template.html')
```

How it Works
============

- As Django starts up and your apps are initialized, your decorated shortcodes are registered.
- When staff users edit a richtext page, metadata about your shortcodes is injected into the page by a Django view and rendered into menus/buttons by javascript. When a button is clicked, its `ModelForm` is rendered into a dialog. When submitted, a placeholder html element is added to store a reference to the `ModelForm` and primary key of the instance.
- When users view a richtext page, the placeholders are parsed, the `ModelForm` instances retrieved and passed into their associated function, and the placeholders are replaced with the return value.

Developing
==========

Installation
------------

This will give you an editable installation.

```sh
python setup.py develop
```

Messing around with the Example Project
---------------------------------------

```sh
cd example_project
python manage.py createdb --noinput
python manage.py runserver
```

Then go to `127.0.0.1:8000/admin`, log in with `admin` / `default`, and edit a Page to see the extra toolbar menus/buttons.

Running the Tests
-----------------

- To run browser tests, install python dependencies with `pip install -U -r dev-requirements.txt -c dev-constraints.txt`.
- To run browser tests headless, [install phantomjs](http://phantomjs.org/download.html) on your system. A `ghostdriver.log` file is created (and deleted after every TestCase) which may be useful for debugging these, though running them again with firefox is generally easier.

```sh
python test [--debug] [<webdriver>]
```

- *--debug* Write verbose output to ghostdriver.log.
- *\<webdriver\>* [phantomjs|firefox|chrome] If ommitted the browser tests will default to phantomjs and fall back to firefox if unavailable.
