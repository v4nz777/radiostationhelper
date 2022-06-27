let invoiceListOpened = false
document.addEventListener("DOMContentLoaded", ()=> {

    //  Hide InvoiceList ON Load
    if(!invoiceListOpened){
        document.querySelectorAll('.solo-modal').forEach(modal => {
            modal.style.display = "none"
        })
    }

    //to hide this modal whenever clicked outside
    document.querySelectorAll('.solo-modal').forEach(modal => {
        const floatBTNCont = document.querySelector('#floatingBTNContract')
        document.addEventListener('click', (event)=> {
            if(event.target != modal && event.target.parentNode != modal && event.target != floatBTNCont && event.target.parentNode != floatBTNCont){
                modal.style.display = "none"

            }
        })
    })


    

})

function loadContract(code) {
    fetch(`/contract/${code}`)
    .then(response => response.json())
    .then(data => {
        console.log(data)
    })
}

function toggleContractInvoiceList(contractid) {
    const invoiceListOpenBTN = document.querySelector(`#openInvoiceListFor-${contractid}`)

    if(invoiceListOpenBTN.style.display == "none"){
        invoiceListOpenBTN.style.display = "flex"
        invoiceListOpened = true
        document.querySelector(`#floatingBtnNotifForContract-${contractid}`).style.display = "none"
    }else{
        invoiceListOpenBTN.style.display = "none"
        invoiceListOpened = false
        //document.querySelector(`#floatingBtnNotifForContract-${contractid}`).style.display = "block"
    }

}



function newInvoice(code){
    document.querySelector(`#submitInvoice-${code}`).classList.add('disabled')
    document.querySelector(`#submitInvoice-${code}`).innerHTML = `<div class="spinner-border" role="status" style="height:16px!important;width:16px!important;"></div>`
    
    fetch('/new_invoice/', {
        method: "POST",
        body: JSON.stringify({
            contract: document.querySelector(`#dataNewInvoiceContract-${code}`).innerHTML,
            invoice_no: document.querySelector(`#dataNewInvoice-${code}`).value,
            from: document.querySelector(`#dataInvoiceFrom-${code}`).value,
            till: document.querySelector(`#dataInvoiceTo-${code}`).value,
        })
    })
    .then(response => response.json())
    .then(data => {
        console.log(data)
        document.querySelector(`#submitInvoice-${code}`).classList.remove('btn-primary')
        document.querySelector(`#submitInvoice-${code}`).classList.add('btn-success')
        document.querySelector(`#submitInvoice-${code}`).innerHTML = checkLarge
        location.reload()
        
    })
}