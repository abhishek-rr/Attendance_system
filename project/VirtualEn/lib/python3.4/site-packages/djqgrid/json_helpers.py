import json

"""
This module contains helper methods to help put function names in the JSON that is used as the jqGrid's options

The jqGrid's option object may contain event handlers, this should appear like so in JavaScript:

    $("#grid").jqGrid({
        loadComplete: loadCompleteHandler
    });

The jqGrid option object is actually a Python dictionary that is rendered to JSON in the jqgrid template tag.

Unfortunately, Python's ``json`` module can't output such JSON, it will always put quotes around strings (without the
quotes, it's not legal JSON), so we need to work around it to support unquoted strings.

The solution is simple and a bit ugly - we use a token that we wrap around function names. We serialize
the dictionary to a JSON string, look for the token and remove the quotes around it.

Our token is ``@@``. So in the example about, our Python dict will be: ``{'loadComplete': '@@loadCompleteHandler@@')``.
When we create the JSON, we remove the quotes and the @@, and end up with the expected string.

The ``function`` helper function puts the token around the string, so that we can build our dictionary like so:
``d = {'loadComplete': function('loadCompleteHandler'))`` .

Instead of using ``json.dumps`` we have our own ``dumps`` that unquotes function names.
"""

token = '@@'

def function(funcname):
    """
    Wraps a JavaScript function name with our token, so it can be unquoted when rendering to JSON.

    The jqGrid option object is actually a Python dictionary that is rendered to JSON in the jqgrid template tag.

    Unfortunately, Python's ``json`` module can't output such JSON, it will always put quotes around strings (without the
    quotes, it's not legal JSON), so we need to work around it to support unquoted strings.

    The solution is simple and a bit ugly - we use a token that we wrap around function names. We serialize
    the dictionary to a JSON string, look for the token and remove the quotes around it.

    Our token is ``@@``. So in the example about, our Python dict will be: ``{'loadComplete': '@@loadCompleteHandler@@')``.
    When we create the JSON, we remove the quotes and the @@, and end up with the expected string.

    The ``function`` helper function puts the token around the string, so that we can build our dictionary like so:
    ``d = {'loadComplete': function('loadCompleteHandler'))`` .

    Args:
        funcname - the function's name

    Returns:
        The wrapped function name
    """
    return token + funcname + token

def dumps(o, *args, **kwargs):
    """
    Serializes an object to JSON, unquoting function names.

    Args:
        o: Object to serialize
        *args: Additional arguments passed to ``json.dumps``
        **kwargs: Additional arguments passed to ``json.dumps``
    """
    s = json.dumps(o, *args, **kwargs)
    s = s.replace('"' + token, '')
    s = s.replace(token + '"', '')
    return s
