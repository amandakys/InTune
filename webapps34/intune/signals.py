import json
import sys
from django.db.models.signals import m2m_changed

from .models import Composition, Notification
from channels import Group


def user_added(sender, **kwargs):
    composition = kwargs['instance']
    model = kwargs['model']
    profile_ids = kwargs['pk_set']
    msg = composition.owner.user.username + ' shared composition "' + composition.title + '" with you!'

    try:
        notification = Notification.objects.get(composition=composition)
    except Notification.DoesNotExist:
        notification = Notification.objects.create(composition=composition, msg=msg)

    for id in profile_ids:
        if not notification.recipients.filter(id=id):
            profile = model.objects.get(id=id)
            notification.recipients.add(profile)
            Group("notif-%s" % profile.id).send({
                "text": json.dumps({
                    "msg": str(msg) + str(profile.id),
                })
            })

if not 'test' in sys.argv:
    m2m_changed.connect(user_added, sender=Composition.users.through)
