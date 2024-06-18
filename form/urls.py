from django.urls import path
from . import views

urlpatterns = [
    path('<int:telegram_id>/', views.TestFormView.as_view(), name='test_form'),
]
