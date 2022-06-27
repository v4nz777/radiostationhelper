
from django.http import JsonResponse
import json
from .helper import transmitter_logging
from django.views.decorators.csrf import csrf_exempt



@csrf_exempt
def log_transmitter(request):
    data = json.loads(request.body)
    if request.method == "POST":
        voltage = data['voltage']
        exciter = data['exciter']
        driver_ipa = data['driver_ipa']
        driver_fwd_pwr = data['driver_fwd_pwr']
        driver_rfl_pwr = data['driver_rfl_pwr']
        vpa = data['vpa']
        final_ipa = data['final_ipa']
        final_fwd_pwr = data['final_fwd_pwr']
        final_rfl = data['final_rfl']
        remarks = data['remarks']
        populate_previous = data['populate']
        sign_on_time = 4
        

        transmitter_logging(voltage,
                            exciter,
                            driver_ipa,
                            driver_fwd_pwr,
                            driver_rfl_pwr,
                            vpa,
                            final_ipa,
                            final_fwd_pwr,
                            final_rfl,
                            remarks,
                            sign_on_time,
                            populate_previous
                            )
        return JsonResponse({'message': 'SUCCESS'})
