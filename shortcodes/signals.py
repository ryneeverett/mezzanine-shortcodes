from django.db.models.signals import pre_save, pre_delete

from mezzanine.core.models import RichText

from . import state
from .register import Shortcode
from .utils import ShortcodeSoup


def _delete_tags(tags):
    for tag in tags:
        shortcode = Shortcode.from_func(tag.get('data-name'))
        instance = shortcode.get_instance(pk=tag.get('data-pk'))
        instance.delete()


def _get_subclasses(klass):
    """ Adapted from http://stackoverflow.com/a/29106313/1938621. """
    result = [klass]
    classes_to_inspect = [klass]
    while classes_to_inspect:
        class_to_inspect = classes_to_inspect.pop()
        for subclass in class_to_inspect.__subclasses__():
            if subclass not in result:
                result.append(subclass)
                classes_to_inspect.append(subclass)
    return result


def on_save(sender, **kwargs):
    instance = kwargs['instance']
    soup = ShortcodeSoup(instance.content)
    tags = set(
        soup.find_all('div', 'data-pending', class_='mezzanine-shortcodes'))

    # Save pending model instances, but only if they're still referenced in the
    # content.
    for tag in tags:
        model_instance = state.PENDING_INSTANCES.pop(tag['data-pending'])
        # Save model instance.
        model_instance.save()
        # Replace the data-pending attribute with data-pk.
        del tag['data-pending']
        tag['data-pk'] = model_instance.pk
    instance.content = str(soup)

    # Delete any shortcode model instances that were removed since the last
    # content save.
    if instance.pk is not None and (not kwargs['update_fields'] or
                                    'content' in kwargs['update_fields']):
        old_instance = sender.objects.get(pk=instance.pk)
        old_tags = set(ShortcodeSoup(old_instance.content).find_shortcodes())

        _delete_tags(old_tags.difference(tags))


def on_delete(sender, **kwargs):
    # Delete all associated shortcode model instances.
    _delete_tags(ShortcodeSoup(kwargs['instance'].content).find_shortcodes())


for subclass in _get_subclasses(RichText):
    pre_save.connect(on_save, subclass)
    pre_delete.connect(on_delete, subclass)
