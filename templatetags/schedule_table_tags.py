from django import template
from PartyShiftSchedule.models import Slot

register = template.Library()


@register.filter(is_safe=True)
def schedule_table_row(row):
    return """
        <tr>
            <td class="shift-schedule-head-col">{0}</td>
            {1}
        </tr>
    """.format(row[0], '\n'.join(map(to_td, row[1:])))


@register.inclusion_tag('PartyShiftSchedule/table_entry_block.html')
def table_block(time, position):
    entrys = Slot.objects.filter(time=time, position=position)
    return {
        'entrys': list(entrys),
        'free_slot': len(entrys) < position.pref_users
    }


def to_td(value):
    return "<td>{0}</td>".format(value)


def toggle_button(user):
    return "<a class=tableToggleButton>{0}</a>".format(user)