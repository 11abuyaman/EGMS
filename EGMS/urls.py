from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from services.views import PatientSignup, LoginRedirect, Profile, CancelAppointment, DepartmentsList, \
    DepartmentAppointments, Home, BookAppointment, EditProfile

urlpatterns = [
                  path('admin/', admin.site.urls),
                  path('accounts/', include('django.contrib.auth.urls')),
                  path('accounts/signup/', PatientSignup.as_view(), name='signup'),
                  path('', Home.as_view(), name='home'),
                  path('login/redirect/', LoginRedirect.as_view(), name='login-redirect'),

                  path('profile/edit/', EditProfile.as_view(), name='edit-profile'),
                  path('profile/<int:pk>/', Profile.as_view(), name='profile'),

                  path('cancel-appointment/', CancelAppointment.as_view(), name='cancel-appointment'),
                  path('book-appointment/', BookAppointment.as_view(), name='book-appointment'),

                  path('departments/', DepartmentsList.as_view(), name='departments'),
                  path('departments/<int:pk>', DepartmentAppointments.as_view(), name='department'),

              ] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) + static(settings.MEDIA_URL,
                                                                                           document_root=settings.MEDIA_ROOT)
