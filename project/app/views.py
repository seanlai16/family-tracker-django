from .models import User, History, GeoFence, Family
from rest_framework.decorators import api_view
from rest_framework.response import Response
import uuid


# Create your views here.


ok = 200
bad = 400

missing_parameter = Response({"data": {}, "message": "Missing parameter"}, status=bad)
invalid_parameter = Response({"data": {}, "message": "Invalid parameter"}, status=bad)


@api_view(['POST', ])
def register_family(request):
    family_name = request.POST.get('family_name')
    displayname = request.POST.get('displayname')
    email = request.POST.get('email')
    phone = request.POST.get('phone')

    if family_name is None or displayname is None or phone is None or email is None:
        return missing_parameter

    family = Family(name=family_name)
    family.save()

    code = generate_code()

    user = User(username=displayname+code, displayname=displayname, family=family, code=code, is_parent=True, email=email, phone=phone)
    user.save()

    return Response({"data": serialize_user(user),
                     "message": "Registration Successful"}, status=ok)


@api_view(['POST',])
def login(request):
    code = request.POST.get('code')

    if code is None:
        return missing_parameter

    try:
        user = User.objects.get(code=code)

        return Response({"data": serialize_user(user),
                         "message": "Login Successful"}, status=ok)

    except User.DoesNotExist:
        return error_response("Invalid Code")


@api_view(['POST',])
def update_user(request):
    uid = request.POST.get('uid')
    displayname = request.POST.get('displayname')
    is_active = request.POST.get('is_active')
    fid = request.POST.get('fid')
    is_parent = request.POST.get('is_parent')
    email = request.POST.get('email')
    phone = request.POST.get('phone')

    if displayname is None or is_active is None or fid is None or is_parent is None or email is None or phone is None:
        return missing_parameter

    if int(is_active) is not 1 and int(is_active) is not 0:
        return invalid_parameter

    if int(is_parent) is not 1 and int(is_parent) is not 0:
        return invalid_parameter

    if uid is None or uid is '': # create new user

        try:
            family = Family.objects.get(pk=fid)
            code = generate_code()
            user = User(username=displayname+code, displayname=displayname, family=family, code=code,
                        is_parent=True if is_parent is '1' else False, email=email, phone=phone, is_active=True)
            user.save()

            return Response({"data": serialize_user(user),
                             "message": "User Created"}, status=ok)

        except Family.DoesNotExist:
            return error_response("Invalid fid")

    else:

        try:
            user = User.objects.get(pk=uid)
            user.displayname = displayname
            user.is_parent = True if is_parent is '1' else False
            user.is_active = True if is_active is '1' else False
            user.email = email
            user.phone = phone
            user.save()

            return Response({"data": serialize_user(user),
                             "message": "User Updated"}, status=ok)

        except User.DoesNotExist:
            return error_response("Invalid uid")


@api_view(['GET',])
def get_user_list(request):
    fid = request.GET.get('fid')

    if fid is None:
        return missing_parameter

    try:
        family = Family.objects.get(pk=fid)
        users = User.objects.filter(family=family, is_active=True)
        user_list = list(map(lambda x: serialize_user(x), users))

        return Response({"data": user_list}, status=ok)

    except Family.DoesNotExist:
        return error_response("Invalid fid")


@api_view(['GET',])
def get_geofence_list(request):
    uid = request.GET.get('uid')

    if uid is None:
        return missing_parameter

    try:
        user = User.objects.get(pk=uid)
        geofences = GeoFence.objects.filter(user=user, is_active=True)
        geofence_list = list(map(lambda x: serialize_geofence(x), geofences))

        return Response({"data": geofence_list}, status=ok)

    except User.DoesNotExist:
        return error_response("Invalid uid")


@api_view(['GET',])
def get_history_list(request):
    uid = request.GET.get('uid')

    if uid is None:
        return missing_parameter

    try:
        user = User.objects.get(pk=uid)
        historys = History.objects.filter(user=user)
        history_list = list(map(lambda  x: serialize_history(x), historys))

        return Response({"data": history_list}, status=ok)

    except User.DoesNotExist:
        return error_response("Invalid uid")


@api_view(['GET',])
def get_last_known_list(request):
    fid = request.GET.get('fid')

    if fid is None:
        return missing_parameter

    try:
        family = Family.objects.get(pk=fid)
        users = User.objects.filter(family=family)
        historys = list(map(lambda  x: get_last_known_location(x), users))
        history_list = list(map(lambda x: serialize_history(x), historys))

        return Response({"data": history_list}, status=ok)

    except Family.DoesNotExist:
        return error_response("Invalid fid")


@api_view(['POST',])
def update_geofence(request):
    gid = request.POST.get('gid')
    name = request.POST.get('name')
    radius = request.POST.get('radius')
    lat = request.POST.get('lat')
    long = request.POST.get('long')
    uid = request.POST.get('uid')
    is_active = request.POST.get('is_active')

    if name is None or radius is None or lat is None or long is None or uid is None or is_active is None:
        return missing_parameter

    if int(radius) is None:
        return invalid_parameter

    if int(is_active) is not 1 and int(is_active) is not 0:
        return invalid_parameter

    if gid is None or gid is '':
        try:
            user = User.objects.get(pk=uid)
            geofence = GeoFence(user=user, name=name, radius=radius, lat=lat, long=long)
            geofence.save()

            return Response({"data": serialize_geofence(geofence),
                             "message": "Geofence created"}, status=ok)

        except User.DoesNotExist:
            return error_response("Invalid uid")

    else:
        try:
            geofence = GeoFence.objects.get(pk=gid)
            geofence.name = name
            geofence.radius = int(radius)
            geofence.lat = lat
            geofence.long = long
            geofence.is_active = True if is_active is '1' else False

            return Response({"data": serialize_geofence(geofence),
                             "message": "Geofence updated"}, status=ok)

        except GeoFence.DoesNotExist:
            return error_response("Invalid gid")


@api_view(['POST',])
def upload_location(request):
    uid = request.POST.get('uid')
    lat = request.POST.get('lat')
    long = request.POST.get('long')
    is_emergency = request.POST.get('is_emergency')

    if uid is None or lat is None or long is None or is_emergency is None:
        return missing_parameter

    if int(is_emergency) is not 1 and int(is_emergency) is not 0:
        return invalid_parameter

    try:
        user = User.objects.get(pk=uid)
        history = History(user=user, lat=lat, long=long, is_emergency=True if is_emergency is '1' else False)

        return Response({"data": serialize_history(history),
                         "message": "Location Uploaded"}, status=ok)

    except User.DoesNotExist:
        return error_response("Invalid uid")


@api_view('POST',)
def upload_geofence(request):
    uid = request.POST.get('uid')
    gid = request.POST.get('gid')
    is_enter =request.POST.get('is_enter')

    if uid is None or gid is None or is_enter is None:
        return missing_parameter

    if int(is_enter) is not 1 and int(is_enter) is not 0:
        return invalid_parameter

    try:
        user = User.objects.get(pk=uid)
        geofence = GeoFence.objects.get(pk=gid)
        history = History(user=user, geofence=geofence, is_enter=True if is_enter is '1' else False)

        return Response({"data": serialize_history(history),
                         "message": "Location Uploaded"}, status=ok)

    except User.DoesNotExist:
        return error_response("Invalid uid")
    except GeoFence.DoesNotExist:
        return error_response("Invalid gid")


def error_response(message):
    return Response({"data": {}, "message": message}, status=bad)


def get_last_known_location(user):
    return History.objects.filter(user=user).order_by('-id')[0]


def serialize_history(history):

    return None if history is None else {
        "id": history.id,
        "timestamp": history.timestamp,
        "lat": history.lat,
        "long": history.long,
        "user": {
            "id": history.user.id,
            "displayname": history.user.displayname
        },
        "geofence": None if history.geofence is None else {
            "id": history.geofence.id,
            "name": history.geofence.name,
            "lat": history.geofence.lat,
            "long": history.geofence.long,
            "radius": history.geofence.radius
        },
        "is_enter": history.is_enter,
        "is_emergency": history.is_emergency
    }


def serialize_geofence(geofence):
    return {
        "id": geofence.id,
        "name": geofence.name,
        "lat": geofence.lat,
        "long": geofence.long,
        "radius": geofence.radius,
        "is_active": geofence.is_active,
        "user": {
            "id": geofence.user.id,
            "displayname": geofence.user.displayname
        }
    }



def serialize_user(user):
    return {
        "id": user.id,
        "displayname": user.displayname,
        "username": user.username,
        "code": user.code,
        "phone": user.phone,
        "email": user.email,
        "is_parent": user.is_parent,
        "is_active": user.is_active,
        "family": {
            "id": user.family.id,
            "name": user.family.name
        }
    }


def generate_code():

    code = uuid.uuid4().hex[:6].upper()

    while is_code_unique(code) is False:
        code = uuid.uuid4().hex[:6].upper()

    return code


def is_code_unique(code):

    try:
        user = User.objects.get(code=code)
        return False
    except User.DoesNotExist:
        return True
