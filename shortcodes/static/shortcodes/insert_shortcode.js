(function($) {
  var editor = window.parent.tinymce.activeEditor,
      SHORTCODES = window.parent.SHORTCODES,
      dialog = SHORTCODES.activeDialog,
      new_elem =
    "<div " +
    "class='mezzanine-shortcodes fresh-shortcode' " +
    "data-name='" + dialog.name + "' " +
    "data-pending='" + $(document).find('script').data('pending') + "' " +
    "></div>" +
    "<p></p>";  // Otherwise no way to navigate below shortcode in textbox.

  if (dialog.isNew) {
    editor.insertContent(new_elem);
  } else {
    dialog.$elem.replaceWith(new_elem);
  }

  $(editor.getDoc()).find('.mezzanine-shortcodes.fresh-shortcode').each(function() {
    SHORTCODES.render.apply(this);
    $(this).removeClass('fresh-shortcode');
  });

  editor.windowManager.close();
})(window.parent.jQuery);
