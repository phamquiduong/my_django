function disabledForm(formID) {
  const form = document.getElementById(formID)
  form.querySelectorAll('input, select, textarea, button').forEach(el => {
    el.disabled = true
  })
}
