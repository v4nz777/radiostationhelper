document.addEventListener('DOMContentLoaded', ()=> {
    
    
    //IN MAIN TAB
    if(window.location.pathname == "/"){
        //Load User API
        loadUSR(userName);

 
        if(document.querySelector("#clockInButton")){
            const clockInBTN = document.querySelector("#clockInButton")
            clockInBTN.addEventListener('click', ()=> {
                logUSR()
                document.querySelector('#clockInCloak').style.display = 'none';
                document.querySelector('#logStatus').classList.remove('bg-danger');
                document.querySelector('#logStatus').classList.add('bg-success');
            })
        }

        hoverToggle('logStatus', 'LOG OUT?', logStatusBTN)

        collapsePasswordChangeToggle('Password')

        document.querySelector('#submitEdited').addEventListener('click', ()=> {
            
            fetch('save_profile/', {
                method: 'POST',
                body: JSON.stringify({
                    email: document.querySelector("#userEmail").value,
                    mobile: document.querySelector("#userMobile").value,
                    telephone: document.querySelector("#userTelephone").value,
                    facebook: document.querySelector("#userFacebook").value,
                    address: document.querySelector("#userAddress").value,
                    change_pass_active: document.querySelector("#collapsePasswordInput").checked,
                    old_password: document.querySelector("#userOldPass").value,
                    new_password: document.querySelector("#userNewPass").value,
                    confirmation: document.querySelector("#userConfirmationPass").value,
                })
            })
            .then(response => response.json())
            .then(data => {
                const profileUpdateAlert = document.createElement('div')
                if(data.alert == "danger" && data.error_fields == "old_fields") {    
                    type = data.alert
                    document.querySelector("#oldKey").classList.add('text-danger')
                    profileUpdateAlert.innerHTML = '<div class="alert alert-' + type + ' alert-dismissible" role="alert">' + data.message + '<button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button></div>'
                    document.querySelector("#profileAlertPlaceholder").append(profileUpdateAlert)
                }else if(data.alert == "danger" && data.error_fields == "new_fields") {
                    type = data.alert
                    document.querySelector("#newKey").classList.add('text-danger')
                    document.querySelector("#confirmationKey").classList.add('text-danger')
                    profileUpdateAlert.innerHTML = '<div class="alert alert-' + type + ' alert-dismissible" role="alert">' + data.message + '<button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button></div>'
                    document.querySelector("#profileAlertPlaceholder").append(profileUpdateAlert)
                }
                else{location.reload()}
                
            })
            
            
        })
    }

    // IN OVERVIEW TAB
    if(window.location.pathname == "/overview/"){
        collapseCaretToggle('People')
        collapseCaretToggle('Department')   
    }else{
        //hiding these buttons//Purpose: To make sure changing positions only in Overview#People's Tab
        document.querySelectorAll(".change-button").forEach(button => {
            button.style.display = 'none'
        })
    }
     
});



    function loadUSR(username) {
        fetch(`usr_api/${username}`)
        .then(response => response.json())
        .then(data => {
            document.querySelector('#profileName').innerHTML = `${data.first_name} ${data.last_name}`;
            document.querySelector('#profilePosition').innerHTML = data.position;
            
            if(data.email){
                document.querySelector('#profileEmail').innerHTML = data.email;
            }else{document.querySelector('#liProfileEmail').style.display = 'none'}
            
            if(data.mobile){
                document.querySelector('#profileMobile').innerHTML = data.mobile;
            }else{document.querySelector('#liProfileMobile').style.display = 'none'}

            if(data.telephone){
                document.querySelector('#profileTele').innerHTML = data.telephone;
            }else{document.querySelector('#liProfileTele').style.display = 'none'}

            if(data.facebook){
                document.querySelector('#profileFacebook').innerHTML = data.facebook;
            }else{document.querySelector('#liProfileFacebook').style.display = 'none'}

            if(data.address){
                document.querySelector('#profileAdd').innerHTML = data.address;
            }else{document.querySelector('#liProfileAdd').style.display = 'none'}
            
            
            
            
            
            if(data.logged){ 
                document.querySelector('#logStatus').classList.add('bg-success')
            }else{document.querySelector('#logStatus').classList.add('bg-danger')}
        })
    } 


    function logUSR() {
        fetch('clock_in/')
        .then(response => response.json())
        .then(data => {
            console.log(data.message)
        })
    }

    function collapseCaretToggle(category) {

        document.querySelector(`#collapse${category}`).addEventListener('hidden.bs.collapse', ()=> {
            document.querySelector(`#collapse${category}BTN`).innerHTML = caretRight
        })
        document.querySelector(`#collapse${category}`).addEventListener('shown.bs.collapse', ()=> {
            document.querySelector(`#collapse${category}BTN`).innerHTML = caretDown
        })
    }

    function collapsePasswordChangeToggle(idKey) {

        document.querySelector(`#collapse${idKey}`).addEventListener('hidden.bs.collapse', ()=> {
            document.querySelector(`#collapse${idKey}Status`).innerHTML = sheild
            document.querySelector(`#collapse${idKey}Input`).checked = false
        })
        document.querySelector(`#collapse${idKey}`).addEventListener('shown.bs.collapse', ()=> {
            document.querySelector(`#collapse${idKey}Status`).innerHTML = sheildFill
            document.querySelector(`#collapse${idKey}Input`).checked = true
        })
    }

    function hoverToggle(subject, hoverInElement, hoverOutElement){
        document.querySelector(`#${subject}`).addEventListener('mouseover', ()=> {
            document.querySelector(`#${subject}`).innerHTML = hoverInElement
        })
        document.querySelector(`#${subject}`).addEventListener('mouseout', ()=> {
            document.querySelector(`#${subject}`).innerHTML = hoverOutElement
        })
    }

    function set_or_create_Position(personUsername) {
        //SETTING OR CREATING POSITION
            
            fetch('/appoint_to_position/', {
                method: 'POST',
               body: JSON.stringify({
                    user: document.querySelector(`#profileUser-${personUsername}`).innerHTML,
                    position: document.querySelector(`#positionsDataList-${personUsername}`).value,
                })    
            })
            .then(response => response.json())
            .then(data => {
                location.reload()
                console.log(data.message)
                //console.log(document.querySelector(`#positionsDataList-${personUsername}`).value)
            })          
    }

    function addPeopleToDept(department) {
        
        fetch('/designate/', {
            method: 'POST',
            body: JSON.stringify({
                person: document.querySelector(`#departmentDataList-${department}`).value,
                department: department
            })
        })
        .then(response => response.json())
        .then(data => {
            console.log(data)  
            location.reload()
        })    
    }



    function assignInCharge(department) {
        fetch('/designate_oic/', {
            method: 'POST',
            body: JSON.stringify({
                person: document.querySelector(`#inChargeDataList-${department}`).value,
                department: department
            })
        })
        .then(response => response.json())
        .then(data => {
            const globalMessenger = document.createElement('div')
            globalMessenger.innerHTML = `<div class="alert alert-danger alert-dismissible fade show" role="alert">
                                            ${data.message}.
                                            <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
                                            </div>`
            //document.querySelector('#globalMessenger').append(globalMessenger)
            location.reload();
        })    
    }

    function sideCollapse() {
       
        document.querySelectorAll(".side-collapse").forEach(container => {
            if(container.style.width == '0px'){
                container.style.width = '275px'
                document.querySelector('#sideCollapseBTN').innerHTML = caretLeftFill
            }else{
                container.style.width = '0px'
                document.querySelector('#sideCollapseBTN').innerHTML = caretRightFill

            }
            
        })
    }