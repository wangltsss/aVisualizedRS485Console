
(function () {
  'use strict'

  // Fetch all the forms we want to apply custom Bootstrap validation styles to
  let forms = document.querySelectorAll('.needs-validation')

  // Loop over them and prevent submission
  Array.prototype.slice.call(forms)
    .forEach(function (form) {
      form.addEventListener('submit', function (event) {
        if (!form.checkValidity()) {
          event.preventDefault()
          event.stopPropagation()
        }

        form.classList.add('was-validated')
      }, false)
    })
})()

function reload(){
  location.reload()
}

function testMode(){
  let val = document.getElementById('test-select').value
  let board_div = document.getElementById('board-id-div')
  let id_input = document.getElementById('board-id-input')
  if (val === 'single'){
    board_div.style.display = 'none'
    id_input.required = false
  }
  else if (val === 'multiple'){
    board_div.style.display = ''
    id_input.required = true
  }
}













