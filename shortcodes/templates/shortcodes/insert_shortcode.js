(function($) {
  var dialog = window.parent.SHORTCODES.activeDialog,
      editor = window.parent.tinymce.activeEditor,
      html = '{{ html }}';

  // Insert element.
  if (dialog.isNew) {
    var current_node = editor.selection.getNode();

    if (current_node.nodeName.toLowerCase() === 'body') {
      $(current_node).append(html);
    } else {
      $(current_node).after(html);
    }
  } else {
    $(dialog.$elem).replaceWith(html);
  }

  // Close dialog.
  editor.windowManager.close();

  // Move cursor below shortcode element. Adapted from
  // http://stackoverflow.com/a/19836226/1938621.
  editor.selection.select(
    $(editor.getBody())
      .find('.mezzanine-shortcodes[data-pending="{{ pending_id }}"]')
      .next()
      .get()[0],
    true
  );
  editor.selection.collapse(false);
})(window.parent.jQuery);
