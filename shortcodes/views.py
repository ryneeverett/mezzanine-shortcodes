import json
import uuid

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
def dialog(request, name):
    """ Serve the modelform for a new shortcode instance in a dialog box. """
    modelformclass = state.SHORTCODES[name].modelform

    if request.method == 'POST':
        modelform = modelformclass(request.POST)
        if modelform.is_valid():
            pending_id = (
                request.GET['pending'] if 'pending' in request.GET else
                uuid.uuid4().hex)
            state.PENDING_INSTANCES[pending_id] = modelform.instance
            return HttpResponse(
                "<script src='{src}' data-pending='{pending_id}'>"
                "</script>".format(
                    src=staticfiles.static('shortcodes/insert_shortcode.js'),
                    pending_id=pending_id))
    else:
        if 'pk' in request.GET:  # edit saved instance
            model = modelformclass._meta.model.objects.get(
                pk=request.GET['pk'])
            modelform = modelformclass(instance=model)
        elif 'pending' in request.GET:  # edit pending instance
            modelform = state.PENDING_INSTANCES[pending_id]
        else:  # new instance
            modelform = modelformclass()

    return render(request, 'shortcodes/dialog.html', {'form': modelform})
