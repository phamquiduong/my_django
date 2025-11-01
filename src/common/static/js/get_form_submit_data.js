function getFormSubmitAsJSON(event) {
  event.preventDefault()
  const formData = new FormData(event.target)
  return Object.fromEntries(formData.entries())
}
