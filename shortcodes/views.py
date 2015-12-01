import json

from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.staticfiles.templatetags import staticfiles
from django.contrib.admin.views.decorators import staff_member_required

from . import state


@staff_member_required
def metadata(request):
    """ Gather shortcode metadata and return it in a javascript file. """
    attributes = [
        'name', 'displayname', 'tooltip', 'iconurl', 'buttontype', 'buttons']
    data = [{attr: getattr(shortcode, attr, False) for attr in attributes}
            for shortcode in state.TOOLBAR]

    return HttpResponse("window.SHORTCODES = {{toolbar: {data}}};".format(
        data=json.dumps(data)))


@staff_member_required
def new(request, name):
    modelformclass = state.SHORTCODES[name].modelform

    if request.method == 'POST':
        modelform = modelformclass(request.POST)
        if modelform.is_valid():
            modelform.save()
            return HttpResponse(
                "<script src='{src}' data-pk='{pk}'></script>".format(
                    src=staticfiles.static('shortcodes/insert_shortcode.js'),
                    pk=modelform.instance.pk))
    else:
        try:
            pk = request.GET['pk']
        except KeyError:  # new instance
            modelform = modelformclass()
        else:  # edit instance
            model = modelformclass._meta.model.objects.get(pk=pk)
            modelform = modelformclass(instance=model)

    return render(request, 'shortcodes/dialog.html', {'form': modelform})
