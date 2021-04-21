import datetime
import json

from motor.models import Controller, Data, Mode

from django.http import HttpResponse
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt

def register(request, req_mac):
    if Controller.objects.filter(mac=req_mac):
        print("Invalid Register %s" % req_mac)
        return HttpResponse("Invalid Register")
    else:
        q = Controller.register(req_mac)
        q.save()
        print("%s registered" % req_mac)
        return HttpResponse("Registered")

@csrf_exempt
def update(request, up_mac):
    qs = Controller.objects.filter(mac=up_mac)
    if qs:
        req = json.loads(request.body)
        up_speed = req['speed_data']
        up_duty = req['duty']
        up_timestamp = req['timestamp']
        tz = datetime.timezone(datetime.timedelta(hours=9))
        up_datetime = datetime.datetime.fromtimestamp(int(up_timestamp) // 1000, tz)

        controller = qs.get()
        controller.speed_data = up_speed
        controller.duty = up_duty
        controller.updated_last = up_datetime
        controller.save()

        data = Data.register(controller.mac, up_speed, up_duty, up_datetime)
        data.save()

        print("%s updated" % up_mac)
        return HttpResponse("%d%d" % (controller.speed_target, controller.mode))
    else:
        print("Invalid Update %s" % up_mac)
        return HttpResponse("Invalid Update")


def mode(request, parm_mac, parm_mode):
    qs = Controller.objects.filter(mac=parm_mac)
    if qs:
        controller = qs.get()
        controller.speed_target = 0
        controller.controlled_last = timezone.now()
        if parm_mode == 'on':
            controller.mode = Mode.ON
        elif parm_mode == 'off':
            controller.mode = Mode.OFF
        elif parm_mode == 'disconnect':
            controller.mode = Mode.DISCON
        else:
            print("Invalid mode Access %s-%s" % (parm_mac, parm_mode))
            return HttpResponse("Invalid mode Access ")

        controller.save()
        print("Mode Updated %s-%s" % (parm_mac, parm_mode))
        return HttpResponse("Mode Updated")

    else:
        print("Invalid mode Access %s" % parm_mac)
        return HttpResponse("Invalid mode Access ")


def change_speed(request, parm_mac, parm_speed):
    qs = Controller.objects.filter(mac=parm_mac)
    if qs:
        controller = qs.get()
        controller.speed_target = parm_speed
        controller.controlled_last = timezone.now()
        controller.save()
        print("Speed Updated %s-%s" % (parm_mac, parm_speed))
        return HttpResponse("Speed Updated")

    else:
        print("Invalid speed Access %s" % parm_mac)
        return HttpResponse("Invalid speed Access ")
