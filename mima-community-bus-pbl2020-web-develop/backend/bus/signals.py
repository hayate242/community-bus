from django.db.models.signals import post_save
import re
from django.core.mail import send_mail
from datetime import datetime

from .models import WatchingNotificationSentences, WatchOverBoardings


def monitoring_notification(sender, **kwargs):
    """
    見守り情報の登録時メール通知を送信
    """
    # loaddata時はメール送信をしない
    if kwargs.get("raw", False):
        return

    # 最新の見守り情報を取得
    watch_over_boarding = WatchOverBoardings.objects.latest("created_at")

    # メール送信
    message = WatchingNotificationSentences.objects.all().first().sentence
    message = re.sub(r'{{bus-stop}}', watch_over_boarding.bus_stop.bus_stop_name, message)
    message = re.sub(r'{{datetime}}',
                    watch_over_boarding.send_at.strftime("%Y年%m月%d日%H時%M分"),
                    message)
    message = re.sub(r'{{name}}', watch_over_boarding.card.name, message)
    for user_for_card in watch_over_boarding.card.user_card_set.all():
        recipient_list = []
        recipient_list.append(user_for_card.user.email)
        parent_name = "{} 様".format(user_for_card.user.username)

        message = re.sub(r'{{parent-name}}', parent_name, message)
        send_mail(
            subject="みまっぷ利用通知",
            message=message,
            from_email=None,
            recipient_list=recipient_list,
            fail_silently=False
        )


post_save.connect(monitoring_notification, sender=WatchOverBoardings)
