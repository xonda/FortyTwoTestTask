from django import template
from django.core import urlresolvers

register = template.Library()


class EditLinkNode(template.Node):
    def __init__(self, obj):
        self.obj = template.Variable(obj)

    def render(self, context):
        obj_pk = self.obj.resolve(context).pk
        return urlresolvers.reverse('admin:hello_info_change', args=(obj_pk,))


@register.tag()
def edit_link(render, token):
    try:
        tag_name, obj = token.split_contents()
    except ValueError:
        raise template.TemplateSyntaxError("%r tag requires a single argument"
                                           % token.contents.split()[0])
    return EditLinkNode(obj)
