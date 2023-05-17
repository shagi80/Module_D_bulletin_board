""" сигналы """
from django.db.models.signals import post_save
from django.dispatch import receiver
from mail.views import mail_comment_accepted, mail_comment_created, mail_comment_not_accepted
from .models import Comment
from .views import comment_not_accepted


@receiver(post_save, sender=Comment)
def send_save_notification(sender, **kwargs):
    """ отправка уведомлений записи/принятии комментария """
    
    instance = kwargs['instance']
    if instance.advert.author.email:
        if kwargs['created']:
            # отправка уведомления автору объявления при создании комментария
            mail_comment_created(instance)
        else:
            # отправка уведомления автору комментария при принятии
            if kwargs['update_fields'] and 'accepted' in kwargs['update_fields']:
                mail_comment_accepted(instance)
        

@receiver(comment_not_accepted, sender=Comment)
def send_not_accepted_notification(sender, **kwargs):
    """ отправка уведомлений автору комментария
    после не принятия (удаления) комментария """

    instance = kwargs['instance']
    if instance.author.email:
        mail_comment_not_accepted(instance)