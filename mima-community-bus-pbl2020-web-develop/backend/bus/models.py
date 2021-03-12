from django.db import models
from django.utils import timezone
from django_boost.models.mixins import LogicalDeletionMixin

from mimaAPI.settings import AUTH_USER_MODEL


# BIG INT UNSIGNED AUTO_INCREMENT
class PositiveBigIntAutoField(models.BigAutoField):
    def db_type(self, connection):
        return 'BIGINT UNSIGNED AUTO_INCREMENT'

    def rel_db_type(self, connection):
        return 'BIGINT UNSIGNED'


class TimeStampMixin(models.Model):
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)

    class Meta:
        abstract = True


# 車両管理マスタ
class MasterBuses(TimeStampMixin, LogicalDeletionMixin):
    id = PositiveBigIntAutoField(primary_key=True)
    bus_name = models.CharField(max_length=64)
    bus_number = models.CharField(max_length=64)

    class Meta:
        db_table = 'm_buses'

    def as_dict(self):
        return {
            'bus_id': f'{self.id}',
            'bus_name': self.bus_name,
        }


# 委託バス会社管理マスタ
class MasterBusCompany(TimeStampMixin):
    id = PositiveBigIntAutoField(primary_key=True)
    name = models.CharField(max_length=64)

    class Meta:
        db_table = 'm_bus_company'


# コース管理マスタ
class MasterCourse(TimeStampMixin, LogicalDeletionMixin):
    id = PositiveBigIntAutoField(primary_key=True)
    user = models.ForeignKey(AUTH_USER_MODEL, models.PROTECT)
    course_name = models.CharField(max_length=64)

    class Meta:
        db_table = 'm_course'

    def as_dict(self):
        return {
            'course_id': f'{self.id}',
            'course_name': self.course_name
        }


# 路線管理マスタ
class MasterRoutes(TimeStampMixin, LogicalDeletionMixin):
    id = PositiveBigIntAutoField(primary_key=True)
    user = models.ForeignKey(AUTH_USER_MODEL, models.PROTECT)
    route_name = models.CharField(max_length=64)
    bus_stops = models.ManyToManyField(
        'MasterBusStops', through='RouteBusStops', related_name='routes')

    class Meta:
        db_table = 'm_routes'

    def as_dict(self):
        return {
            'route_id': f'{self.id}',
            'route_name': self.route_name
        }


# 便管理マスタ
class MasterRouteOrders(TimeStampMixin):
    id = PositiveBigIntAutoField(primary_key=True)
    route = models.ForeignKey(
        'MasterRoutes', models.PROTECT, related_name='route_order_set')
    course = models.ForeignKey(
        'MasterCourse', models.PROTECT, related_name='route_order_set')
    order = models.IntegerField()
    route_bus_stops = models.ManyToManyField(
        'RouteBusStops', through='RouteOrderBusStops')

    class Meta:
        db_table = 'm_route_orders'

    def as_dict(self):
        return {
            'route_order_id': f'{self.id}',
            'route_order_name': f'第{self.order}便'
        }


# バス停管理マスタ
class MasterBusStops(TimeStampMixin, LogicalDeletionMixin):
    # id = PositiveBigIntAutoField(primary_key=True)
    bus_stop_name = models.CharField(max_length=64)
    longitude = models.FloatField()
    latitude = models.FloatField()
    is_passing_point = models.BooleanField()

    class Meta:
        db_table = 'm_bus_stops'

    def as_dict(self):
        return {
            'bus_stop_id': f'{self.id}',
            'bus_stop_name': self.bus_stop_name,
            'longitude': f'{self.longitude}',
            'latitude': f'{self.latitude}'
        }


# 経由地点管理マスタ
class MasterViaPoints(TimeStampMixin):
    id = PositiveBigIntAutoField(primary_key=True)
    longitude = models.FloatField()
    latitude = models.FloatField()

    class Meta:
        db_table = 'm_via_points'


# 運賃金額管理
class MasterFares(TimeStampMixin, LogicalDeletionMixin):
    id = PositiveBigIntAutoField(primary_key=True)

    class GROUP(models.TextChoices):
        CASH_ADULT = '大人 - 現金'
        CASH_CHILD = '小人 - 現金'
        CASH_HANDICAPPED_ADULT = '障害者（大） - 現金'
        CASH_HANDICAPPED_CHILD = '障害者（小） - 現金'
        COUPON_ADULT = '大人 - 回数券'
        COUPON_CHILD = '小人 - 回数券'
        COUPON_HANDICAPPED = '障害者 - 回数券'
        COMMUTER_PASS = '定期券'
        FREE = '無料'
        COUPON_ADULT_SALE = '大人 - 回数券販売'
        COUPON_CHILD_SALE = '小人 - 回数券販売'
        COUPON_HANDICAPPED_SALE = '障害者 - 回数券販売'
        GET_OFF = '降車'

    group = models.CharField(
        choices=GROUP.choices,
        max_length=32
    )
    amount = models.PositiveIntegerField()

    class Meta:
        db_table = 'm_fares'


#　繰り返し管理マスタ
class MasterRepeats(TimeStampMixin):
    id = PositiveBigIntAutoField(primary_key=True)
    sunday = models.BooleanField()
    monday = models.BooleanField()
    tuesday = models.BooleanField()
    wednesday = models.BooleanField()
    thursday = models.BooleanField()
    friday = models.BooleanField()
    saturday = models.BooleanField()

    class Meta:
        db_table = 'm_repeats'


# ICカード管理マスタ
class MasterCards(TimeStampMixin, LogicalDeletionMixin):
    id = PositiveBigIntAutoField(primary_key=True)
    card_number = models.CharField(max_length=16)
    name = models.CharField(max_length=64, blank=True, null=True)

    class Meta:
        db_table = 'm_cards'


# 業務開始・終了管理
class WorkStartEnd(TimeStampMixin):
    id = models.BigAutoField(primary_key=True)
    bus = models.ForeignKey('MasterBuses', models.PROTECT)
    course = models.ForeignKey('MasterCourse', models.PROTECT)
    driver = models.ForeignKey('users.Users', models.PROTECT)
    money = models.PositiveIntegerField()
    trip_meter = models.PositiveIntegerField()
    send_at = models.DateTimeField()

    class FLAG(models.IntegerChoices):
        START = 0
        END = 1

    work_start_end_flag = models.IntegerField(choices=FLAG.choices)

    class Meta:
        db_table = 'work_start_end'


# システム通知管理
class SystemNotifications(TimeStampMixin):
    id = models.BigAutoField(primary_key=True)
    notification_message = models.CharField(max_length=256)

    class Meta:
        db_table = 'system_notifications'


# 乗車数管理
class Boardings(TimeStampMixin):
    id = models.BigAutoField(primary_key=True)
    bus = models.ForeignKey('MasterBuses', models.PROTECT)
    route_order = models.ForeignKey('MasterRouteOrders', models.PROTECT)
    bus_stop = models.ForeignKey('MasterBusStops', models.PROTECT)
    driver = models.ForeignKey('users.Users', models.PROTECT)
    fare = models.ForeignKey('MasterFares', models.PROTECT)
    bus_stop_order = models.IntegerField()
    memo = models.TextField(max_length=256, blank=True)
    number = models.PositiveIntegerField()
    send_at = models.DateTimeField()

    class Meta:
        db_table = 'boardings'


# 見守り乗降履歴管理
class WatchOverBoardings(TimeStampMixin):
    id = models.BigAutoField(primary_key=True)
    card = models.ForeignKey('MasterCards', models.PROTECT)
    bus = models.ForeignKey('MasterBuses', models.PROTECT)
    bus_stop = models.ForeignKey('MasterBusStops', models.PROTECT)
    driver = models.ForeignKey('users.Users', models.PROTECT)
    send_at = models.DateTimeField()
    boarding_type = models.IntegerField()

    class Meta:
        db_table = 'watch_over_boardings'


# 車両点検管理
class VehicleInspections(TimeStampMixin):
    id = models.BigAutoField(primary_key=True)
    bus = models.ForeignKey('MasterBuses', models.PROTECT)
    driver = models.ForeignKey('users.Users', models.PROTECT)
    chack_fuel = models.BooleanField()
    chack_engine = models.BooleanField()
    chack_brake = models.BooleanField()
    chack_wiper = models.BooleanField()
    chack_horn = models.BooleanField()
    chack_turn_signal = models.BooleanField()
    chack_light = models.BooleanField()
    chack_mirror = models.BooleanField()
    chack_instrument = models.BooleanField()
    chack_tire = models.BooleanField()
    chack_exhaust_sound = models.BooleanField()
    chack_cooling_water = models.BooleanField()
    chack_battery = models.BooleanField()
    chack_door = models.BooleanField()
    chack_inside = models.BooleanField()
    remark = models.CharField(max_length=1024, blank=True)

    class Meta:
        db_table = 'vehicle_inspections'


# 見守り通知文管理
class WatchingNotificationSentences(TimeStampMixin):
    id = models.BigAutoField(primary_key=True)
    # boarding_type = models.PositiveIntegerField()
    sentence = models.TextField()

    class Meta:
        db_table = 'watching_notification_sentences'


# 路線バス停管理
class RouteBusStops(TimeStampMixin):
    id = models.BigAutoField(primary_key=True)
    route = models.ForeignKey(
        'MasterRoutes', models.PROTECT,
        related_name='relation_bus_stop'
    )
    bus_stop = models.ForeignKey('MasterBusStops', models.PROTECT)
    order = models.PositiveIntegerField()

    class Meta:
        db_table = 'route_bus_stops'
        unique_together = ('route', 'order')


# 便バス停管理
class RouteOrderBusStops(TimeStampMixin):
    id = models.BigAutoField(primary_key=True)
    route_order = models.ForeignKey(
        'MasterRouteOrders', models.PROTECT,
        related_name='route_order_bus_stops_set'
    )
    route_bus_stop = models.ForeignKey('RouteBusStops', models.PROTECT)
    arrival_time = models.TimeField(default="00:00")
    is_enabled = models.BooleanField()

    class Meta:
        db_table = 'route_order_bus_stops'
        #unique_together = ('route_order', 'route_bus_stop')
        ordering = 'route_bus_stop__order',


# お知らせ
class Notifications(TimeStampMixin):
    id = models.BigAutoField(primary_key=True)
    notifications_sentence = models.TextField()

    class Meta:
        db_table = 'notifications'


# お知らせ変更予約
class NotificationChangeRequests(TimeStampMixin):
    id = models.BigAutoField(primary_key=True)
    notification_id = models.BigIntegerField()
    notifications_sentence = models.TextField()
    start_from = models.DateTimeField(blank=True, null=True)
    end_at = models.DateTimeField(blank=True, null=True)
    repeat_id = models.BigIntegerField(blank=True, null=True)

    class Meta:
        db_table = 'notification_change_requests'


# ICカード紐付け管理
class UserCards(TimeStampMixin, LogicalDeletionMixin):
    id = models.BigAutoField(primary_key=True)
    card = models.ForeignKey(
        'MasterCards', models.PROTECT, related_name="user_card_set")
    user = models.ForeignKey(AUTH_USER_MODEL, models.PROTECT)

    class Meta:
        db_table = 'user_cards'
