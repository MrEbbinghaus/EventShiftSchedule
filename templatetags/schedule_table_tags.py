from django import template

register = template.Library


@register.filter(is_safe=True)
def schedule_tablerow(time, args):
    return """
        <tr>
            <td>{0}</td>

        <tr>
    """.format(time)
