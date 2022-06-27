document.addEventListener('DOMContentLoaded', ()=> {

    if(location.pathname == "/worktab/"){
    
        document.querySelector("#collapseAdsList").addEventListener('shown.bs.collapse', ()=> {
            document.querySelector("#collapseAdsListBTN").innerHTML = eyez
        })
        
        document.querySelector("#collapseAdsList").addEventListener('hidden.bs.collapse', ()=> {
            document.querySelector("#collapseAdsListBTN").innerHTML = eyeSlash
        })
    }

    if(location.pathname == "/worktab/"){
        document.querySelector("#collapseCollectionsList").addEventListener('shown.bs.collapse', ()=> {
            document.querySelector("#collapseCollectionsListBTN").innerHTML = piggyBankFill
        })
        
        document.querySelector("#collapseCollectionsList").addEventListener('hidden.bs.collapse', ()=> {
            document.querySelector("#collapseCollectionsListBTN").innerHTML = piggyBank
        })
    }

    if(location.pathname == "/worktab/"){
        const paymentInvoiceInput = document.querySelector('#dataPaymentInvoiceNo')
        paymentInvoiceInput.addEventListener('keyup', ()=> {
            populateNewPayment(paymentInvoiceInput.value)
        })
    }

    //SET DEFAULT FILTERED INVOICES BY MONTH
    if(location.pathname == "/worktab/"){
        const today = new Date()
        const mm = String(today.getMonth() + 1).padStart(2, '0');
        const yyyy = today.getFullYear()

        document.querySelector('#filterCollections').value = `${yyyy}-${mm}`
    }

    //populate invoices collections
    if(location.pathname == "/worktab/"){
        //set inital when load
        queryCollections(document.querySelector('#filterCollections').value)
        //change when filtered
        document.querySelector('#filterCollections').addEventListener('change', ()=> {
            queryCollections(document.querySelector('#filterCollections').value)
        })
    }

 

})




function addNewAds(){
    document.querySelector('#submitAdvertisement').classList.add('disabled')
    document.querySelector('#submitAdvertisement').innerHTML = `<div class="spinner-border" role="status" style="height:16px!important;width:16px!important;"></div>`

    fetch('/new_ads/', {
        method: "POST",
        body: JSON.stringify({
            title: document.querySelector('#dataAdTitle').value,
            code: document.querySelector('#dataAdCode').value,
            amount: document.querySelector('#dataAdAmount').value,
            customer: document.querySelector('#dataAdCompany').value,
            customer_address: document.querySelector('#dataAdCompanyAddress').value,
            category: document.querySelector('#dataAdCategory').value,
            account_executive: document.querySelector('#dataAdAE').value,
            broadcast_start: document.querySelector('#dataAdBroadcastStart').value,
            broadcast_end: document.querySelector('#dataAdBroadcastEnd').value,
            spots_per_day: document.querySelector('#dataAdSpots').value,
            material_duration: document.querySelector('#dataAdDuration').value,
            sponsorship_taglines: document.querySelector('#dataAdTagline').value,
            specific_time_schedule: document.querySelector('#dataAdTimeSched').value,
            remarks: document.querySelector('#dataAdRemarks').value
        })
    })
    .then(response => response.json())
    .then(data => {
        console.log(data)
        document.querySelector('#submitAdvertisement').classList.remove('btn-primary')
        document.querySelector('#submitAdvertisement').classList.add('btn-success')
        document.querySelector('#submitAdvertisement').innerHTML = checkLarge
        //location.href = `/contract/${document.querySelector('#dataAdCode').value}`
        window.open(`/contract/${document.querySelector('#dataAdCode').value}`, '_blank')
    })
}





function populateNewPayment(invoice_no){
    fetch(`/populate_new_payment/${invoice_no}`, {
        method: 'GET'
    })
    .then(response => response.json())
    .then(data => {
        const amountComma = data.ad_amount.toLocaleString({style: 'currency'})
        document.querySelector('#dataPaymentPayor').innerHTML = ""
        document.querySelector('#dataPaymentAmount').innerHTML = "" 
        document.querySelector('#dataPaymentPayor').innerHTML = `&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="fw-bold">Payor:<small class="fw-normal text-success"> ${data.advertiser}<\small></span>`
        document.querySelector('#dataPaymentAmount').innerHTML = `&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="fw-bold">Amount:<small class="fw-normal text-success"> ₱${amountComma}<\small></span>`
        if(data.valid){
            document.querySelector('#submitNewPayment').classList.remove('disabled')
        }else{
            document.querySelector('#submitNewPayment').classList.add('disabled')
            document.querySelector('#dataPaymentPayor').innerHTML = ""
            document.querySelector('#dataPaymentAmount').innerHTML = "" 
            document.querySelector('#dataPaymentPayor').innerHTML = `&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="fw-bold">Payor:<small class="fw-normal text-danger"> ${data.advertiser}<\small></span>`
            document.querySelector('#dataPaymentAmount').innerHTML = `&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="fw-bold">Amount:<small class="fw-normal text-danger"> ${amountComma}<\small></span>`
        }

    })
    .catch(()=> {
        document.querySelector('#submitNewPayment').classList.add('disabled')
            document.querySelector('#dataPaymentPayor').innerHTML = ""
            document.querySelector('#dataPaymentAmount').innerHTML = "" 
            document.querySelector('#dataPaymentPayor').innerHTML = `&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="fw-bold">Payor:<small class="fw-normal text-danger"> Empty<\small></span>`
            document.querySelector('#dataPaymentAmount').innerHTML = `&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="fw-bold">Amount:<small class="fw-normal text-danger"> None<\small></span>`
    })
}

function inputPayment(){
    document.querySelector('#submitNewPayment').classList.add('disabled')
    document.querySelector('#submitNewPayment').innerHTML = `<div class="spinner-border" role="status" style="height:16px!important;width:16px!important;"></div>`
    fetch('/input_payment/', {
        method: "PUT",
        body: JSON.stringify({
            invoice: document.querySelector('#dataPaymentInvoiceNo').value,
            or_num: document.querySelector('#dataPaymentORNum').value,
            or_date: document.querySelector('#dataPaymentORDate').value,
        })
    })
    .then(response => response.json())
    .then(data => {
        console.log(data)
        document.querySelector('#submitNewPayment').classList.remove('btn-primary')
        document.querySelector('#submitNewPayment').classList.add('btn-success')
        document.querySelector('#submitNewPayment').innerHTML = checkLarge
        if(data.succeed){
            location.reload()
        }else{
            document.querySelector('#submitNewPayment').classList.remove('btn-success')
            document.querySelector('#submitNewPayment').classList.remove('disabled')
            document.querySelector('#submitNewPayment').classList.add('btn-primary')
            document.querySelector('#submitNewPayment').innerHTML = 'Submit'
            document.querySelector('#paymentAlert').innerHTML = '<div class="alert alert-danger alert-dismissible" role="alert"><span class="fw-bold">' + data.advertiser + '</span> ' + data.message + '<button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button></div>'
        }
        
    })
}



function queryCollections(monthyear) {
    fetch('/populate_collections/', {
        method: 'POST', 
        body: JSON.stringify({
            month_year: monthyear
        })
    })
    .then(response => response.json())
    .then(data => {
        const collectionList = document.querySelector('#collectionList') 
        collectionList.innerHTML = ''
        data.filtered_invoices.forEach(invoice => {
            console.log(invoice)
            //invoice_no
            let status = 'PAID'
            if(invoice.paid){
                status = 'PAID'
            }else{status = 'UNPAID'}

            let amount = invoice.amount
            if(invoice.amount === null){
                amount = 0
            }else{amount = invoice.amount}
            
            const datum = document.createElement('tr')
            datum.innerHTML = `<th>${invoice.invoice_no}</th>
                                <td>${invoice.invoice_date}</td>
                                <td>${invoice.advertiser}</td>
                                <td>${invoice.particular}</td>
                                <td>${amount}</td>
                                <td>${status}</td>`
            collectionList.append(datum)
        });
    })
}


function newPosition() {
    document.querySelector('#submitPosition').classList.add('disabled')
    document.querySelector('#submitPosition').innerHTML = `<div class="spinner-border" role="status" style="height:16px!important;width:16px!important;"></div>`
    fetch('/new_position/', {
        method: "POST",
        body: JSON.stringify({
            title: document.querySelector('#dataPositionTitle').value,
            level1_salary: document.querySelector('#dataSalary1').value,
            level2_salary: document.querySelector('#dataSalary2').value,
            level3_salary: document.querySelector('#dataSalary3').value,
            level4_salary: document.querySelector('#dataSalary4').value,
            level5_salary: document.querySelector('#dataSalary5').value,
        })
    })
    .then(response => response.json())
    .then(data => {
        console.log(data)
        if(data.success){
            location.reload()
        }
    })
}

function editPosition(position){
    fetch(`/edit_position/${position}`, {
        method: "GET"
    })
    .then(response => response.json())
    .then(data => {
        console.log(data)
        const newButton = document.createElement('div')
        newButton.setAttribute('class', 'badge rounded-pill bg-primary btn')
        newButton.setAttribute('id', `saveThisPositionBTN-${position}`)
        newButton.innerHTML = 'save'


        document.querySelector(`#titleForPosition-${position}`).append(newButton)
        document.querySelector(`#salary1TableFor-${position}`).innerHTML = `<input id="edit1Salary-${position}" type="text" class="form-control" value="${data.salary1}" style="width: 5rem;" autofocus/>`
        document.querySelector(`#salary2TableFor-${position}`).innerHTML = `<input id="edit2Salary-${position}" type="text" class="form-control" value="${data.salary2}" style="width: 5rem;" autofocus/>`
        document.querySelector(`#salary3TableFor-${position}`).innerHTML = `<input id="edit3Salary-${position}" type="text" class="form-control" value="${data.salary3}" style="width: 5rem;" autofocus/>`
        document.querySelector(`#salary4TableFor-${position}`).innerHTML = `<input id="edit4Salary-${position}" type="text" class="form-control" value="${data.salary4}" style="width: 5rem;" autofocus/>`
        document.querySelector(`#salary5TableFor-${position}`).innerHTML = `<input id="edit5Salary-${position}" type="text" class="form-control" value="${data.salary5}" style="width: 5rem;" autofocus/>`
    
        //ON CLICKED SAVE
        document.querySelector(`#saveThisPositionBTN-${position}`).addEventListener('click', ()=> {
            document.querySelector(`#saveThisPositionBTN-${position}`).classList.add('disabled')
            document.querySelector(`#saveThisPositionBTN-${position}`).innerHTML = `<div class="spinner-border" role="status" style="height:16px!important;width:16px!important;"></div>`
            
            
            saveThisPosition(position)
            console.log(saveThisPosition(position))
 
            document.querySelector(`#salary1TableFor-${position}`).innerHTML = data.salary1
            document.querySelector(`#salary2TableFor-${position}`).innerHTML = data.salary2
            document.querySelector(`#salary3TableFor-${position}`).innerHTML = data.salary3
            document.querySelector(`#salary4TableFor-${position}`).innerHTML = data.salary4
            document.querySelector(`#salary5TableFor-${position}`).innerHTML = data.salary5

            location.reload()
            
        })
    
    })
}

function saveThisPosition(position_id) {

    fetch('/save_position', {
        method: "PUT",
        body: JSON.stringify({
            position_id: position_id,
            salary1: document.querySelector(`#edit1Salary-${position_id}`).value,
            salary2: document.querySelector(`#edit2Salary-${position_id}`).value,
            salary3: document.querySelector(`#edit3Salary-${position_id}`).value,
            salary4: document.querySelector(`#edit4Salary-${position_id}`).value,
            salary5: document.querySelector(`#edit5Salary-${position_id}`).value,
        })
    })
    .then(response => response.json())
    .then(data => {
       console.log(data)
    })

}


