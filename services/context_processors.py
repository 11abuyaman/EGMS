from services.models import Department


def defaults(request):
    departments = Department.objects.all()
    return {
        "departments": departments,
    }
