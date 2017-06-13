import json
from django.db.models.signals import m2m_changed

from intune.models import Composition, Notification
from channels import Group


def user_added(sender, **kwargs):
    composition = kwargs['instance']
    model = kwargs['model']
    profile_ids = kwargs['pk_set']
    print("profile ids", profile_ids)
    msg = composition.owner.user.username + ' shared composition "' + composition.title + '" with you!'

    try:
        notification = Notification.objects.get(composition=composition)
    except Notification.DoesNotExist:
        notification = Notification.objects.create(composition=composition, msg=msg)

    for id in profile_ids:
        if not notification.recipients.filter(id=id):
            profile = model.objects.get(id=id)
            notification.recipients.add(profile)
            username = profile.user.username
            print("send notif to ", username)
            Group("notif-%s" % profile.id).send({
                "text": json.dumps({
                    "msg": str(msg) + str(profile.id),
                })
            })
m2m_changed.connect(user_added, sender=Composition.users.through)