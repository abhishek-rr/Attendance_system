import string
from django.template import Context, Template
from django.template.loader import get_template
from json_helpers import function

class Column(object):
    """
    A Column object represents one Grid column

    The Column object defines how a column's value is retrieved and how it is formatted.

    Column is effectively an abstract class - Grids should be using its derived classes.
    """

    # Each column is associated a count, which is used for column ordering in the Grid. This count is generated
    # by using the following class attribute.
    _creation_count = 0

    def __init__(self, title, model_path, **kwargs):
        """
        Initializes a column.

        Args:
            title: The column's title in the grid. title.lower() is the default column name.
            model_path: The column's data field's path in the model.
                For example, if this is the ``Name`` column in a grid of ``Person`` models, and the person's name is
                in the ``fullname`` attribute of the ``Person`` model, ``model_path`` should be ``fullname``.
                ``model_path`` can also access attributes in nested objects: ``innerobj.attr`` will be resolved to
                ``model_instance.innerobj.attr``
            **kwargs: All other arguments are copied as is to the column's ``colModel``.
        """
        self._title = title
        self._colModel = dict(kwargs)
        self._colModel['name'] = title.lower()
        self._count = Column._creation_count
        Column._creation_count += 1
        self._model_path = model_path

    def _get_model_attr(self, attr, model):
        """
        Returns model.attr, taking into account nested attributes.
        """
        return reduce(getattr, attr.split('.'), model)

    def _get_model_value(self, model):
        """
        Returns the column's value in the model

        The default implementation is to use ``get_model_attr``
        """
        return self._get_model_attr(self._model_path, model)

    def render_text(self, model):
        """
        Returns a text representation of the column's value.

        The default implementation is to convert ``get_model_value`` to a unicode string.
        """
        value = self._get_model_value(model)
        if value is None:
            return unicode('')
        return unicode(value)

    def render_html(self, model):
        """
        Returns an HTML representation of the column's value.

        The default implementation is to return the text value.
        """
        return self.render_text(model)

    @property
    def title(self):
        """ Returns the name that goes in the colName JSON """
        return self._title

    @property
    def model(self):
        """ Returns the ``colModel`` """
        return self._colModel

    def get_sort_name(self):
        """
        Returns the column's "sort-name", which is used to apply ordering on a queryset.

        The default implementation is to take the model_path and replace each . with __ .
        """
        return self._model_path.replace('.', '__')

class TextColumn(Column):
    """
    A column that contains simple text strings.

    This is basically just a Column. We create a new class because it seems more tidy.
    """
    pass

class ClientOnlyColumn(Column):
    """
    A column that is filled by the client

    Use a ``ClientOnlyColumn`` when you fill the data in your JavaScript code. The server does nothing with this column.
    """
    def __init__(self, title, **kwargs):
        super(ClientOnlyColumn, self).__init__(title, '', **kwargs)

    def _get_model_value(self, model):
        return ''

class TemplateColumn(Column):
    """
    A column that is rendered by a Django template

    Use a ``TemplateColumn`` when you want the column to contain complex HTML content.

    Due to a bug in jqGrid, cell values cannot contain HTML - it conflicts with inline editing. So instead,
    the cell values returned by the default ``Grid.get_json_data`` method will be the text rendering of the column.
    The HTML data will be placed in the ``html`` property of the row's data.

    To actually display the HTML data we use a formatter, called ``customHtmlFormatter``, which resides in
    ``djqgrid_utils.js``
    """
    def __init__(self, title, model_path, template = None, template_name = None,**kwargs):
        """
        Initializes a TemplateColumn

        Args:
            title: The column's title
            model_path: The column's model path
            template: A Django template that will be rendered
            template_name: A name of a Django template that will be rendered.
            **kwargs: Additional arguments that will be passed directly to the column's ``colModel``

        You can specify a template *or* a template_name, but not both.
        """
        super(TemplateColumn, self).__init__(title, model_path, **kwargs)
        if template:
            self._template = Template(template.strip())
        elif template_name:
            self._template = get_template(template_name)
        else:
            self._template = None # set_template may be called later
        if not 'formatter' in kwargs:
            self._colModel['formatter'] = function('customHtmlFormatter')

    def set_template(self, template):
        self._template = Template(template.strip())

    def _fill_context(self, context, model):
        """
        Fills the template generation context with data from the model.

        The default implementation does nothing. You can override this if your template requires additional
        context data that can be filled from the model.

        Args:
            context - The template context.
            model - The model of the currently rendered row

        Returns:
            The context after it's been updated.
        """
        return context

    def render_html(self, model):
        if not self._template:
            raise ValueError("Template has not been set in %s" % self)
        context = Context({'model': model})
        self._fill_context(context, model)
        html = self._template.render(context = context)

        # jqGrid has issues with multiline cell values, so we make sure the cell value fits in a single line.
        lines = html.split('\n')
        lines = [line.strip() for line in lines]
        html = string.join(lines)

        return html

class LinkColumn(TemplateColumn):
    """
    A column that is rendered as a single ``<a href=...>`` link
    """
    template = """
    <a href="{{ url }}">{{ name }}</a>
    """

    def __init__(self, title, model_path, url_builder, **kwargs):
        """
        Initializes a LinkColumn.

        Args:
            title: The column's title
            model_path: The column's model_path
            url_builder: a function that takes a model and returns the link's URL
            **kwargs: Additional arguments passed directly to the column's ``colModel``
        """
        super(LinkColumn, self).__init__(title, model_path, template=LinkColumn.template, **kwargs)
        self._url_builder = url_builder
        # TODO: Allow url_builder to be a model_path or a function.

    def _fill_context(self, context, model):
        url = self._url_builder(model)
        context['url'] = url
        context['name'] = self._get_model_attr(self._model_path, model)

class CheckboxColumn(Column):
    """
    A column that is rendered as a checkbox.
    """
    def __init__(self, title, model_path, **kwargs):
        kwargs['formatter'] = 'checkbox'
        if 'editable' in kwargs and not 'edittype' in kwargs:
            kwargs['formatoptions'] = {'disabled': False}
            kwargs['edittype'] = 'checkbox'
            kwargs['editoptions'] = {'value': 'true:false'}
        super(CheckboxColumn, self).__init__(title, model_path, **kwargs)

    def render_text(self, model):
        text = super(CheckboxColumn, self).render_text(model)
        return text=='True'    # Turn the field into a boolean, for JavaScript

class KeyColumn(Column):
    """
    A Key column - a column that will contain the row's key.

    This column is hidden by default, and is not rendered.
    """
    def __init__(self, model_path, **kwargs):
        kwargs['key'] = True
        kwargs['hidden'] = True
        super(KeyColumn, self).__init__("Key", model_path, **kwargs)
