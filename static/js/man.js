function cond_select(){
    let selection = document.getElementById("pos-select")
    let idx = selection.selectedIndex
    let val = selection.options[idx].value

    let all_radios = document.getElementsByClassName("tunnl_switch_" + val)
    for (let i = 0; i < all_radios.length; i++){
        all_radios[i].checked = true
    }
}

function disconnect_all(){
    let all_radios = document.getElementsByClassName("tunnl_switch_none")
    for (let i = 0; i < all_radios.length; i++){
        all_radios[i].checked = true
    }
}

function submit_cur_form(form_id, tunnl_id){
    let tunnl = document.getElementById(tunnl_id).checked
    if (!tunnl){
        tunnl = !tunnl
    }
    let form = document.getElementById(form_id)
    form.submit()
}


function SetCookie(sName, sValue) {
    document.cookie = sName + "=" + escape(sValue)

}

function GetCookie(sName) {
    let aCookie = document.cookie.split(";")
    for (let i = 0; i < aCookie.length; i++) {
        let aCrumb = aCookie[i].split("=")
        if (sName === aCrumb[0]) {
            return unescape(aCrumb[1])
        }
    }
    return null
}

function ScrollBack() {
    if (GetCookie("scroll") != null) {
        document.body.scrollTop = GetCookie("scroll")
    }
}

function SubmitForm(fid){
    document.getElementById(fid).submit()
}

function ChangeBoardSubmit(tid){
    document.getElementById('change_board_input').value = tid
    document.getElementById('change-board-form').submit()
}































