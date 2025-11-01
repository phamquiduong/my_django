document.addEventListener('DOMContentLoaded', function () {
  var toastElList = document.querySelectorAll('.toast')
  toastElList.forEach(function (toastEl, index) {
    setTimeout(function () {
      var toast = new bootstrap.Toast(toastEl)
      toast.show()
    }, index * 600)
  })
})
