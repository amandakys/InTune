from django.db.models.signals import m2m_changed

from intune.models import Composition, Notification


def user_added(sender, **kwargs):
    composition = kwargs['instance']
    model = kwargs['model']
    profile_ids = kwargs['pk_set']

    try:
        notification = Notification.objects.get(composition=composition)
    except Notification.DoesNotExist:
        notification = Notification.objects.create(composition=composition, msg=composition.owner.user.username + ' shared ' + composition.title + ' with you.')

    for id in profile_ids:
        profile = model.objects.get(id=id)
        notification.recipients.add(profile)

m2m_changed.connect(user_added, sender=Composition.users.through)