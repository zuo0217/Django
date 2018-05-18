#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# Create time : 12/05/20182:50 PM
# Create by Saseny.Zhou
# File name: serializers.py


from django.contrib.auth.models import User, Group
from rest_framework import serializers
from api.models import UserManage, UserRecord, APPInfo


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('url', 'username', 'email', 'groups')


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ('url', 'name')


class UserManageSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = UserManage
        fields = ('userName', 'serialNumber', 'unitUUID', 'authorized', 'addTime', 'timeOut')


class UserRecordSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = UserRecord
        fields = ('userName', 'message', 'timeInfo')


class APPInfoSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = APPInfo
        fields = ('appName', 'currentVersion', 'newUpdate', 'continueUser', 'updateInfo')
