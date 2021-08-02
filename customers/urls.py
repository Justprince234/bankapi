from django.urls import path


from .views import ContactList

urlpatterns = [
    path('api/contactlist/', ContactList.as_view()),
]

