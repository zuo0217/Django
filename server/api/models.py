from django.db import models


# Create your models here.


class UserManage(models.Model):
    userName = models.TextField(primary_key=True)
    serialNumber = models.TextField()
    unitUUID = models.TextField()
    authorized = models.BooleanField()
    addTime = models.DateTimeField(auto_now=True)
    timeOut = models.DateTimeField()

    def __str__(self):
        return self.userName


class UserRecord(models.Model):
    userName = models.TextField()
    message = models.TextField()
    timeInfo = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.userName


class APPInfo(models.Model):
    appName = models.TextField(primary_key=True)
    currentVersion = models.TextField(null=True)
    newUpdate = models.BooleanField()
    continueUser = models.BooleanField()
    updateInfo = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.appName
