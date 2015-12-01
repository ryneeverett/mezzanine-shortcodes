(function($) {
  var editor = window.parent.tinymce.activeEditor,
      SHORTCODES = window.parent.SHORTCODES,
      dialog = SHORTCODES.activeDialog,
      pk = $(document).find('script').data('pk');

  var new_elem =
    "<div " +
    "class='mezzanine-shortcodes new-shortcode' " +
    "data-name='" + dialog.name + "' " +
    "data-pk='" + pk + "' " +
    "></div>" +
    "<p></p>";  // Otherwise no way to navigate below shortcode in textbox.

  if (dialog.isEdit) {
    dialog.$elem.replaceWith(new_elem);
  } else {
    editor.insertContent(new_elem);
  }

  $(editor.getDoc()).find('.mezzanine-shortcodes.new-shortcode').each(function() {
    SHORTCODES.render.apply(this);
    $(this).removeClass('new-shortcode');
  });

  editor.windowManager.close();
})(window.parent.jQuery);
