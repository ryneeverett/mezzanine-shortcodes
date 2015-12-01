(function($) {
  $(document).ready(function() {
    tinymce.PluginManager.add('shortcodes', function(editor) {

      var BASEURL = tinymce.baseURI.protocol + '://' + tinymce.baseURI.authority,
          SHORTCODEMETA = {},  // {displayname: [<button>], displayname: [<menubutton>]}
          SHORTCODEREPR = {};  // {name: {displayname: '', image: ''}}

      function render() {
        // Render `this` .mezzanine-shortcodes node to editor.
        var repr = SHORTCODEREPR[this.getAttribute('data-name')];

        if (!!repr.image) {
          this.style['background-image'] = "url('" + BASEURL + repr.image + "')";
        } else {
          this.textContent = repr.displayname;
        }

        // Prevent nested shortcodes.
        this.contentEditable = false;
      }

      function openDialog(displayname, name, $elem) {
        // Based on the example plugin.
        var isEdit = typeof $elem !== 'undefined',
            instance = isEdit ? 'pk=' + $elem.data('pk') : '';

        window.SHORTCODES.activeDialog = {name: name, $elem: $elem, isEdit: isEdit};

        editor.windowManager.open({
          title: displayname,
          url: BASEURL + '/shortcodes/dialog/' + name + '?' + instance,
          width: 600,
          height: 400,
          buttons: [
            {
              text: 'Insert',
              onclick: function() {
                var $iframe = $(editor.windowManager.getWindows()[0].getContentWindow().document);
                $iframe.find('form').submit();
              }
            },
            {text: 'Close', onclick: 'close'}
          ]
        });
      }

      // Render buttons/menus.
      if ('SHORTCODES' in window) {
        window.SHORTCODES.render = render;


        var getDisplayName = function(button) {
          // XXX All displaynames must be unique.
          SHORTCODEMETA[button.displayname] = button;
          SHORTCODEREPR[button.name].displayname = button.displayname;

          if (button.buttontype != 'button' || !button.iconurl) {
            // Free buttons cannot have both displayname and icon.
            return button.displayname;
          }
        },

            getIconUrl = function(shortcode) {
          if (shortcode.iconurl) {
            SHORTCODEREPR[shortcode.name].image = shortcode.iconurl;
            return shortcode.iconurl + '?name=' + shortcode.name;
          } else {
            return shortcode.iconurl;
          }
        },

            openDialogFromElem = function(elem) {
          var displayname = $.trim(elem.control.settings.text),
            // Sometimes the click triggers on the button and sometimes on it's nested element.
              $elem = $(($(elem.target).is('button')) ? elem.target.firstChild : elem.target);

          if (!displayname) {
            // From http://stackoverflow.com/a/22633877/1938621.
            var iconurl = $elem.css('background-image').replace(/^url\(['"]?/,'').replace(/['"]?\)$/,''),

                name = iconurl.replace(/.*\?name=/g, '');

            displayname = SHORTCODEREPR[name].displayname;
          }

          var meta = SHORTCODEMETA[displayname];
          openDialog(displayname, meta.name);
        };

        $.each(window.SHORTCODES.toolbar, function (i, shortcode) {
          SHORTCODEREPR[shortcode.name] = {};

          var config = {
            text: getDisplayName(shortcode),
            tooltip: shortcode.tooltip,
            image: getIconUrl(shortcode),
            icon: false,
            type: shortcode.buttontype,
          };
          switch (shortcode.buttontype) {
            case 'button':
              config.onclick = openDialogFromElem;
              break;
            case 'menubutton':
              // Based on createFormatMenu in formatControls.js.
              function createMenu(buttons) {
                return $.map(buttons, function(button) {
                  SHORTCODEREPR[button.name] = {};

                  var menuItem = {
                    text: getDisplayName(button),
                    icon: 'shortcodes',
                    image: getIconUrl(button),
                  };

                  // TODO Implement nested menus.
                  // if (button.items) {
                    // menuItem.menu = createMenu(button.items);
                  // }

                  return menuItem;
                });
              }

              config.menu = {
                type: 'menu',
                items: createMenu(shortcode.buttons),
                onclick: openDialogFromElem,
              };
              break;
            default:
              console.warn(
                'Attempted to add button of unknown type: ' + shortcode.buttontype);
              break;
          }
          editor.addButton(shortcode.name, config);
        });
      } else {
        console.error('Shortcodes data not found. This is probably a server issue.');
      }

      // Render shortcode representations in the textbox.
      editor.on('init', function(e) {
        $(e.target.getDoc()).find('.mezzanine-shortcodes').each(render);
      });

      // Allow editing shortcodes via the contextmenu.
      editor.addMenuItem('shortcode', {
        text: 'Edit Shortcode',
        onPostRender: function() {

          function handleDisabledState(ctrl, selector) {
            // Adapted from http://stackoverflow.com/a/19458918/1938621.
            function bindStateListener() {
              ctrl.visible(editor.dom.getParent(editor.selection.getStart(), selector));
              editor.selection.selectorChanged(selector, function(state) {
                ctrl.visible(state);
              });
            }

            if (editor.initialized)
              bindStateListener();
            else
              editor.on('init', bindStateListener);
          }

          handleDisabledState(this, 'div.mezzanine-shortcodes');
        },
        onclick: function() {
          var $elem = $(editor.selection.getNode()),
              name = $elem.data('name'),
              displayname = SHORTCODEREPR[name].displayname;
          openDialog(displayname, name, $elem);
        },
      });
    });
  });
})(jQuery);
