import json
from django.db.models.signals import m2m_changed

from intune.models import Notification, Composition
from channels import Group


def user_added(**kwargs):
    action = kwargs['action']
    if (action == "pre_add") or (action == "pre_remove"):
        return

    composition = kwargs['instance']
    model = kwargs['model']
    profile_ids = kwargs['pk_set']

    if action == "post_add":
        msg = composition.owner.user.username + ' shared composition "' + composition.title + '" with you!'

    # action == "post_remove"
    else:
        msg = composition.owner.user.username + ' removed you from composition "' + composition.title + '"'

    notification = Notification.objects.create(composition=composition, msg=msg)

    for pid in profile_ids:
        profile = model.objects.get(id=pid)
        notification.recipients.add(profile)

        Group("notif-%s" % profile.id).send({
            "text": json.dumps({
                "msg": str(msg),})
        })


m2m_changed.connect(user_added, sender=Composition.users.through)
