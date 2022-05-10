from django.urls import path
from . import views

urlpatterns = [
    path('post/', views.post_mac, name='postMacs'),
    # path('home/', views.home, name='home')
    path('macsList/', views.MacsList.as_view(), name='test'),
    path('macsListView/', views.MacListView.as_view(), name='view'),
    path('check/', views.CheckMac.as_view(), name='check'),
    path('upgrade/', views.up_grade, name='upgrade'),
    # path('purchases/?<mac>/', views.PurchaseList.as_view()),
]