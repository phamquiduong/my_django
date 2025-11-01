async function callAPI(url, method, body) {
  const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value

  try {
    const res = await fetch(
      url,
      {
        method: method,
        credentials: 'include',
        headers: {
          'Content-Type': 'application/json',
          'X-CSRFToken': csrfToken,
        },
        body: JSON.stringify(body)
      }
    )

    let jsonData = await res.json()
    jsonData = (res.ok) ? { success: true, ...jsonData } : { success: false, ...jsonData }
    return jsonData
  } catch (err) {
    return {
      success: false,
      message: err.message,
    }
  }
}
