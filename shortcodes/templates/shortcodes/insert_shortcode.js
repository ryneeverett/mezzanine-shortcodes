(function($) {
  var editor = window.parent.tinymce.activeEditor,
      SHORTCODES = window.parent.SHORTCODES,
      dialog = SHORTCODES.activeDialog,
      html = "{{ html }}";

  if (dialog.isNew) {
    editor.insertContent(html);
  } else {
    dialog.$elem.replaceWith(html);
  }

  $(editor.getDoc()).find('.mezzanine-shortcodes.fresh-shortcode').each(function() {
    SHORTCODES.render.apply(this);
    $(this).removeClass('fresh-shortcode');
  });

  editor.windowManager.close();
})(window.parent.jQuery);
