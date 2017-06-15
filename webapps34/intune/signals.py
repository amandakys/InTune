from channels import Group
from django.db.models.signals import m2m_changed
import json
import sys

from .models import Composition, Notification

def user_added(**kwargs):
    action = kwargs['action']
    if (action == "pre_add") or (action == "pre_remove"):
        return

    composition = kwargs['instance']
    model = kwargs['model']
    profile_ids = kwargs['pk_set']

    msg = "%s %s %s" % (str(composition.owner.user),
                        "shared" if action == "post_add" else "removed",
                        str(composition))

    notification = Notification.objects.create(composition=composition, msg=msg)

    for pid in profile_ids:
        profile = model.objects.get(id=pid)
        notification.recipients.add(profile)

        Group("notif-%s" % profile.user.id).send({
            "text": json.dumps({
                "msg": str(msg),})
        })

if 'test' not in sys.argv:
    m2m_changed.connect(user_added, sender=Composition.users.through)
