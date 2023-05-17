""" представления почтовых сообщений """

from datetime import timedelta
from django.utils import timezone
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.contrib.sites.models import Site
from django.urls import reverse
from django.contrib.auth.models import User
from b_board.settings import DEFAULT_FROM_EMAIL
from advert.models import Advert


def send_comment_mail(user, url, comment, subject_text, body_text):
    """ отпрака письма о создании/изменения комментария """

    # рендеринг HTML шаблона
    html_content = render_to_string(
            'mail/comment_mail.html',
            {'comment': comment, 'user': user,
             'url': url, 'body_text': body_text}
        )
    # подготовка сообщения
    msg = EmailMultiAlternatives(
            subject = subject_text,
            body = body_text,
            from_email = DEFAULT_FROM_EMAIL,
            to = [user.email,]
        )                
    # привязка HTML и отправка
    msg.attach_alternative(html_content, "text/html")
    msg.send()   


def mail_comment_created(comment):
    """ подготовка уведомления о создании комментария """

    user = comment.advert.author
    url = Site.objects.get_current().domain \
        + reverse('one_advert', args=[comment.advert.pk])\
        + f'#comment_div_{comment.pk}'
    subject_text =  'Новый комментарий к вашему объявлению'
    body_text = f'Здравствуй, {user.username}. Новый комментарий к вашему объявлению !'

    send_comment_mail(user, url, comment, subject_text, body_text)            


def mail_comment_accepted(comment):
    """ подготовка уведомления о принятии комментария """
 
    user = comment.author
    url = Site.objects.get_current().domain \
        + reverse('one_advert', args=[comment.advert.pk])\
        + f'#comment_div_{comment.pk}'
    subject_text = 'Ваш комментарий принят автором объявления'
    body_text = f'Здравствуй, {user.username}. Ваш комментарий принят автором объявления !'

    send_comment_mail(user, url, comment, subject_text, body_text)
 

def mail_comment_not_accepted(comment):
    """ подготовка уведомления об удалении комментария автором объявления """
    
    user = comment.author
    url = Site.objects.get_current().domain \
        + reverse('one_advert', args=[comment.advert.pk])
    subject_text = 'Ваш комментарий отклонен автором объявления'
    body_text = f'Здравствуй, {user.username}. Ваш комментарий отклонен автором объявления !'

    send_comment_mail(user, url, comment, subject_text, body_text)
 

def send_weekly_messages():
    """ отправка новых объявлений за неделю """

    # выбираем новости за прошедшие 7 дней
    new_adverts = Advert.objects.filter(
        created_at__gte=(timezone.now() - timedelta(days=27))
        )
    domain = Site.objects.get_current().domain
    # проходим по списку пользователей
    for user in User.objects.all():
        if user.email:
            # исключаем объявления, созданные этим пользователем
            user_new_adverts = new_adverts.exclude(author=user)
            if user_new_adverts:
                # подготовка шаблона и сообщения
                html_content = render_to_string(
                        'mail/weekly_adverts_mail.html',
                        {'adverts': user_new_adverts, 'domain': domain, 'user': user}
                    )
                msg = EmailMultiAlternatives(
                        subject = 'Новые объявления за неделю',
                        body=f'Здравствуй, {user.username}. Узнай что произошло за неделю !',
                        from_email = DEFAULT_FROM_EMAIL,
                        to = [user.email,]
                    )
                # привязка HTML и отправка
                msg.attach_alternative(html_content, "text/html")
                msg.send() 