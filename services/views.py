from datetime import datetime

from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import ListView, DetailView
from rest_framework.response import Response
from rest_framework.views import APIView

from services.forms import SignUpForm, EditProfileForm
from services.mixins import UserIsStaffMixin
from services.models import User, Appointment, Department


class Home(LoginRequiredMixin, View):
    def get(self, request):
        if request.user.type == 'patient':
            return redirect('profile', pk=request.user.pk)


class LoginRedirect(LoginRequiredMixin, View):
    def get(self, request):
        if request.user.type == 'patient':
            return redirect('profile', pk=request.user.pk)


class DepartmentsList(LoginRequiredMixin, ListView):
    model = Department
    # ordering = ['-appointments__date']
    template_name = 'appointments/departments.html'


class DepartmentAppointments(LoginRequiredMixin, View):
    def get(self, request, pk):
        department = Department.objects.get(pk=pk)
        grouped_appointments = {
            "in_week": [],
            "in_month": [],
            "more": []
        }

        appointments = department.appointments.filter(patient=None, date__gte=datetime.today())
        for appointment in appointments:
            if appointment.is_this_week():
                grouped_appointments["in_week"].append(appointment)
            elif appointment.is_this_month():
                grouped_appointments["in_month"].append(appointment)
            else:
                grouped_appointments["more"].append(appointment)

        return render(request, 'appointments/department-details.html', {
            'department': department, 'appointments': grouped_appointments
        })


class PatientSignup(View):
    def post(self, request):
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('departments')
        else:
            return render(request, 'registration/signup.html', {'form': form, 'errors': form.errors.as_data()})

    def get(self, request):
        form = SignUpForm()
        return render(request, 'registration/signup.html', {'form': form})


class Profile(LoginRequiredMixin, View):
    def get(self, request, pk):
        return render(request, 'account/patient-profile.html', {"profile_user": User.objects.get(pk=pk)})


class EditProfile(LoginRequiredMixin, View):
    def get(self, request):
        form = EditProfileForm(instance=request.user)
        return render(request, 'account/edit-profile.html', {"form": form})

    def post(self, request):
        form = EditProfileForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
        return redirect('profile', pk=request.user.pk)


class CancelAppointment(LoginRequiredMixin, APIView):
    def post(self, request):
        user = request.user
        appointment_id = request.POST.get('id', None)
        print(appointment_id)
        try:
            appointment = Appointment.objects.get(id=appointment_id)
            if user.id == appointment.patient.id:
                appointment.patient = None
                appointment.save()
                return Response({'success': True})

        except Appointment.DoesNotExist as e:
            print(e)

        Response({'success': False}, status=403)


class BookAppointment(LoginRequiredMixin, APIView):
    def post(self, request):
        user = request.user
        appointment_id = request.POST.get('id', None)
        print(user)
        try:
            appointment = Appointment.objects.get(id=appointment_id)
            if appointment.patient is None:
                appointment.patient = user
                appointment.save()
                return Response({'success': True})

        except Appointment.DoesNotExist as e:
            print(e)

        Response({'success': False}, status=403)
