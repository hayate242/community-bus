from django.urls import path
from . import views

urlpatterns = [
    path("init/create/", views.WorkStartEndView.as_view()),
    path("inspections/create/", views.BusInspectionPostView.as_view()),
    path("routes/", views.GetBusList.as_view()),
    path("inspections/", views.GetBusInspectionAPI.as_view()),
    path("course/", views.BusCourseList.as_view()),
    path("bus_stops/", views.BusStops.as_view()),
    path("fare/", views.BusFare.as_view()),
    path("boardings/create/", views.BusBoardingNumber.as_view()),
    path("watch_over_boarding/create/", views.PostWatchOverBoarding.as_view()),
    path("course/info/", views.BusCourseInfo.as_view()),
    path("locations/", views.GetBusLocationView.as_view()),
    # path('watch_over_boarding/', views.<クラス名>.as_view()), ← 未実装, iOSに見守り情報の取得いらない？
    path("locations/create/", views.SaveBusLocationView.as_view()),
    path("card/IDm/info/", views.CardInfo.as_view()),
    path("card/IDm/create/", views.CardCreate.as_view()),
]