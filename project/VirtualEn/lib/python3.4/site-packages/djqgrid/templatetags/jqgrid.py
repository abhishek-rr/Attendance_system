# coding=utf-8
from django import template
from djqgrid import json_helpers

register = template.Library()

@register.simple_tag(takes_context=True)
def jqgrid(context, grid, prefix='', pager=True, urlquery=None, **kwargs):
    """
    Adds a complete jqGrid - HTML and JavaScript - to the template.

    Two HTML elements are added, a ``<table id='grid'>`` and a ``<div id='pager'>``. JavaScript code to initialize the
    jqGrid is also added.

    After the grid is set up in the browser, it will access the server again and ask for the grid data. The URL is
    defined in the Grid object, and is appended by the ``urlquery`` argument and the current request's query dict.
    For example, if the template is rendering the URL ``/view?p=1``, the grid's URL is ``/grid/17?g=2`` and
    ``urlquery`` is ``q=3``, the grid's data will be retrieved from ``/grid/17?g=2&q=3&p=1``

    Args:
        context - The template context
        grid - the Grid
        prefix - A prefix for the grid and pager element IDs. The default is no prefix, meaning the elements are
            named ``grid`` and ``pager``. Adding ``prefix='prefix'`` creates elements with the IDs ``prefix-grid``
            and ``prefix-pager``.
        pager - True if a pager is added to the grid. If no pager is added, the row count is set to 99,999.
        urlquery - An additional query string that will be added to the data request that will be sent to the server.
        **kwargs - All additional arguments are added as is to the jqGrid initialization option object.

    Returns:
        The generated HTML
    """
    if prefix and prefix[-1]!='-':
        prefix += '-'  # Append a - to the prefix

    gridId = prefix + "grid"
    pagerId = prefix + "pager"
    options = grid.get_options(kwargs)
    # Add the query dict to the url
    if not '?' in options['url']:
        options['url'] += '?'
    if urlquery:
        options['url'] += urlquery
    options['url'] += context['request'].GET.urlencode()
    if pager:
        options['pager'] = '#' + pagerId
    else:
        options['rowNum'] = 99999
    options = json_helpers.dumps(options, indent=4)

    html = """
    <table id="%s"><tr><td></td></tr></table>
    <div id="%s"></div>
    <script type="text/javascript">
        $(function() {
            $('#%s').jqGrid(%s);
        });
    </script>""" % (gridId, pagerId, gridId, options);

    return html
