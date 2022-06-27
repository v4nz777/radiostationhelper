document.addEventListener('DOMContentLoaded', ()=> {
    if(location.path == '/worktab/'){
        document.querySelector('#submitTransmitterLogLoading').style.display = 'none';
    }
})


function submitTransmitterLog() {
    
    document.querySelector('#submitTransmitterLog').classList.add('disabled')
    document.querySelector('#submitTransmitterLog').innerHTML = `<div class="spinner-border" role="status" style="height:16px!important;width:16px!important;"></div>`

    fetch('/log_transmitter/', {
        method: "POST",
        body: JSON.stringify({
            voltage: document.querySelector('#dataVoltage').value,
            exciter: document.querySelector('#dataExciter').value,
            driver_ipa: document.querySelector('#dataDriverIPA').value,
            driver_fwd_pwr: document.querySelector('#dataDriverFWD').value,
            driver_rfl_pwr: document.querySelector('#dataDriverRFL').value,
            vpa: document.querySelector('#dataVPA').value,
            final_ipa: document.querySelector('#dataFinalIPA').value,
            final_fwd_pwr: document.querySelector('#dataFinalFWD').value,
            final_rfl: document.querySelector('#dataFinalRFL').value,
            remarks: document.querySelector('#dataRemarks').value,
            populate: document.querySelector('#dataPopulatePrevious').checked,
        })
    })
    .then(response => response.json())
    .then(data => {
        console.log(data)
        document.querySelector('#submitTransmitterLog').classList.remove('btn-primary')
        document.querySelector('#submitTransmitterLog').classList.add('btn-success')
        document.querySelector('#submitTransmitterLog').innerHTML = checkLarge
        location.reload()
    })
}



