from datetime import datetime
from django.contrib.auth import login, authenticate
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import ListView, DetailView
from rest_framework.response import Response
from rest_framework.views import APIView

from services.filters import PatientsFilter
from services.forms import SignUpForm, EditProfileForm, PeriodicMedicationForm, ResultForm, EditPatientForm, \
    AppointmentForm
from services.mixins import UserIsStaffMixin
from services.models import User, Appointment, Department, Medicine
from django.contrib import messages


class Home(LoginRequiredMixin, View):
    def get(self, request):
        if request.user.type == 'patient':
            return render(request, "home/home.patient.html")
        elif request.user.is_staff:
            return render(request, "home/home.staff.html")


class LoginRedirect(LoginRequiredMixin, View):
    def get(self, request):
        if request.user.type == 'patient':
            return redirect('home')
        elif request.user.is_staff:
            return redirect('home')


class DepartmentsList(LoginRequiredMixin, ListView):
    model = Department
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
            messages.success(request, 'Patient profile updated successfully!')
        else:
            messages.error(request, 'Something went wrong!: {}'.format(form.errors))
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


class PatientsList(UserIsStaffMixin, View):
    def get(self, request):
        filters = PatientsFilter(request.GET, queryset=User.objects.filter(type='patient'))
        patients = filters.qs
        return render(request, 'staff/patients.html', {
            "patients": patients,
            "filters": filters.form
        })


class StaffList(UserIsStaffMixin, View):
    def get(self, request):
        filters = PatientsFilter(request.GET, queryset=User.objects.filter(is_staff=True))
        staff = filters.qs
        form = SignUpForm()
        return render(request, 'staff/staff.html', {
            "staff": staff,
            "filters": filters.form,
            "form": form
        })

    def post(self, request):
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Staff account has been added successfully!")
        else:
            messages.error(request, form.errors)
        return redirect('staff-list')


class NewPeriodicMedication(UserIsStaffMixin, View):
    def get(self, request):
        form = PeriodicMedicationForm()
        form.fields["patient"].queryset = User.objects.filter(type='patient')
        return render(request, 'staff/new-periodic-med.html',
                      {"form": form, "patients": User.objects.filter(type='patient')})

    def post(self, request):
        form = PeriodicMedicationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Periodic medication has been added successfully!")
        else:
            messages.error(request, "Message sent.")

        return redirect('staff-new-pm')


class NewResult(UserIsStaffMixin, View):
    def get(self, request):
        form = ResultForm()
        form.fields["patient"].queryset = User.objects.filter(type='patient')
        return render(request, 'staff/new-result.html', {
            "form": form
        })

    def post(self, request):
        form = ResultForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Result has been added successfully!")
        else:
            messages.error(request, form.errors)

        return redirect('staff-new-result')


class NewAppointment(UserIsStaffMixin, View):
    def get(self, request):
        form = AppointmentForm()
        form.fields["doctor"].queryset = User.objects.filter(type='doctor')
        return render(request, 'staff/new-appointment.html', {
            "form": form,
        })

    def post(self, request):
        form = AppointmentForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Appointment has been added successfully!")
        else:
            messages.error(request, form.errors)

        return redirect('staff-new-appointment')


class VerifyPatient(UserIsStaffMixin, APIView):
    def post(self, request):
        pk = request.POST.get('patient_id', None)
        is_verified = request.POST.get('is_verified', None)
        if is_verified:
            try:
                patient = User.objects.get(id=pk)
                patient.verified = is_verified == 'true'
                patient.save()
                return Response({'success': True})
            except Exception as e:
                print(e)
        return Response({'success': False}, status=403)


class EditPatient(UserIsStaffMixin, APIView):
    def post(self, request):
        try:
            patient_id = request.POST.get('id', None)

            form = EditPatientForm(request.POST, instance=User.objects.get(pk=patient_id))
            if form.is_valid():
                form.save()
                messages.success(request, 'Patient profile updated successfully!')
            else:
                messages.error(request, 'Something went wrong!: {}'.format(form.errors))
        except Exception as e:
            messages.error(request, 'Something went wrong!: {}'.format(e))
        return redirect('staff-patients')


class EditStaff(UserIsStaffMixin, APIView):
    def post(self, request):
        try:
            staff_id = request.POST.get('id', None)
            form = EditPatientForm(request.POST, instance=User.objects.get(pk=staff_id))
            if form.is_valid():
                form.save()
                messages.success(request, 'Staff account updated successfully!')
            else:
                messages.error(request, 'Something went wrong!: {}'.format(form.errors))
        except Exception as e:
            messages.error(request, 'Something went wrong!: {}'.format(e))
        return redirect('staff-list')


class Testing(View):
    def get(self, request):
        dept = Department.objects.get(id=2)
        appointments = dept.appointments.all()

        return render(request, 'testing.html', {'dept_t': dept, 'app': appointments})
