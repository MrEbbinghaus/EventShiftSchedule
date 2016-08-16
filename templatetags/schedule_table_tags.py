from django import template

register = template.Library()


@register.filter(is_safe=True)
def schedule_table_row(row):
    return """
        <tr>
            {0}
        </tr>
    """.format('\n'.join(map(to_td, row)))


def to_td(value):
    return "<td>{0}</td>".format(value)

def toggle_button(user):
    return "<a class=tableToggleButton>{0}</a>".format(user)