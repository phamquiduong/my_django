function generateErrorHTML(errors) {
  const errorMessages = errors.map(
    ({ message, code }) => message
  )
  const errorHtml = errorMessages.reduce((htmlStr, error) => htmlStr + `<li>${error}</li>`, '')
  return `<ul class="text-danger">${errorHtml}</ul>`
}
