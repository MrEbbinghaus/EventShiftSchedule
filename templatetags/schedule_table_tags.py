from django import template
from EventShiftSchedule.models import Slot, otpSlot

register = template.Library()


@register.filter(is_safe=True)
def schedule_table_row(row):
    return """
        <tr>
            <td class="shift-schedule-head-col">{0}</td>
            {1}
        </tr>
    """.format(row[0], '\n'.join(map(to_td, row[1:])))


@register.inclusion_tag('EventShiftSchedule/table_entry_block.html')
def table_block(time, position, user):
    signed_up = signed_up_for(user=user, time=time, position=position)
    entrys = [to_full_name(slot.user) for slot in Slot.objects.filter(time=time, position=position).exclude(user=user)]
    user = to_full_name(user)

    return {
        'entrys': entrys,
        'time_id': time.id,
        'position_id': position.id,
        'free_slot': len(entrys) < position.pref_users or signed_up,
        'precheck': 'checked' if signed_up else 'unchecked',
        'user': user,
    }


@register.inclusion_tag('EventShiftSchedule/otp_table_entry_block.html')
def otp_table_block(oneTimePosition, user):
    signed_up = signed_up_for_otp(user=user, oneTimePosition=oneTimePosition)
    entries = otpSlot.objects.filter(otPosition=oneTimePosition).count()
    user = to_full_name(user)

    return {
        'entries': entries,
        'position_id': oneTimePosition.id,
        'precheck': 'checked' if signed_up else 'unchecked',
        'user': user,
    }


def to_full_name(user):
    if (user.first_name is not '') or (user.last_name is not ''):
        return " ".join([user.first_name, user.last_name])
    return user


def signed_up_for(user, time, position):
    return Slot.objects.filter(user=user, time=time, position=position).exists()


def to_td(value):
    return "<td>{0}</td>".format(value)


def toggle_button(user):
    return "<a class=tableToggleButton>{0}</a>".format(user)

def signed_up_for_otp(user, oneTimePosition):
    return otpSlot.objects.filter(user=user, otPosition=oneTimePosition).exists()