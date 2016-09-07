from django.db.models.signals import pre_save

from mezzanine.core.models import RichText

from . import state
from .utils import ShortcodeSoup


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

for subclass in _get_subclasses(RichText):
    pre_save.connect(on_save, subclass)
