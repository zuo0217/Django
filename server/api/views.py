from django.shortcuts import render
from django.contrib.auth.models import User, Group
from api.models import UserManage, UserRecord, APPInfo
from rest_framework import viewsets
from api.serializers import UserSerializer, GroupSerializer, UserManageSerializer, UserRecordSerializer, \
    APPInfoSerializer
from django.http import JsonResponse
import time


# Create your views here.


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer


class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows group to be viewed or edited
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer


class UserManageViewSet(viewsets.ModelViewSet):
    queryset = UserManage.objects.all()
    serializer_class = UserManageSerializer


class UserRecordViewSet(viewsets.ModelViewSet):
    queryset = UserRecord.objects.all()
    serializer_class = UserRecordSerializer


class AppInfoViewSet(viewsets.ModelViewSet):
    queryset = APPInfo.objects.all()
    serializer_class = APPInfoSerializer


def user_confirm(request):
    if request.method == "GET":
        userName = request.GET.get("userName", False)
        serialNumber = request.GET.get("serialNumber", False)
        userUUID = request.GET.get("unitUUID", False)
        appName = request.GET.get("app", False)
        version = request.GET.get("version", False)
        result = UserManage.objects.filter(userName=userName)
        if result:
            serial_number = UserManage.objects.get(userName=userName).serialNumber
            unit_uuid = UserManage.objects.get(userName=userName).unitUUID
            if serialNumber != serial_number or userUUID != unit_uuid:
                return JsonResponse({"status": False, "message": "Serial Number or UUID info not match."})
            authorized = UserManage.objects.get(userName=userName).authorized
            if authorized is False:
                return JsonResponse({"status": False, "message": "App not authorized."})
            time_out = UserManage.objects.get(userName=userName).timeOut
            current = int(time.time())
            timestamp = int(
                time.mktime(time.strptime("{} 00:00:00".format(str(time_out).split()[0]), '%Y-%m-%d %H:%M:%S')))
            if timestamp < current:
                return JsonResponse({"status": False, "message": "Use authorized Time Out."})
            result = APPInfo.objects.filter(appName=appName)
            if result:
                target_version = APPInfo.objects.get(appName=appName).currentVersion
                newUpdate = APPInfo.objects.get(appName=appName).newUpdate
                continueUser = APPInfo.objects.get(appName=appName).continueUser
                updateInfo = APPInfo.objects.get(appName=appName).updateInfo
                if version == target_version:
                    return JsonResponse({"status": True, "message": "Verify Passed."})
                if newUpdate is True and continueUser is True:
                    return JsonResponse({"status": True, "message": updateInfo})
                if newUpdate is True and continueUser is False:
                    return JsonResponse({"status": False, "message": updateInfo})
            else:
                return JsonResponse({"status": False, "message": "App Info not Found."})
        else:
            return JsonResponse({"status": False, "message": "User Info Not Exist."})


def record_upload(request):
    if request.method == "GET":
        userName = request.GET.get("userName", False)
        message = request.GET.get("message", False)
        if userName is False or message is False:
            return JsonResponse({"status": False, "message": "Incorrect POST arguments."})
        result = UserManage.objects.filter(userName=userName)
        if result:
            try:
                UserRecord.objects.create(userName=userName, message=message)
                return JsonResponse({"status": True, "message": "Upload Record Passed."})
            except:
                JsonResponse({"status": False, "message": "Upload Record Error."})
        else:
            return JsonResponse({"status": False, "message": "UserName not Found."})
