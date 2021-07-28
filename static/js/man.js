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