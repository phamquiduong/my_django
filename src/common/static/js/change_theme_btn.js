const changeThemeModeBtn = document.querySelector('#changeThemeModeBtn')
const updateChangeThemeModeBtn = () => {
  switch (themeMode) {
    case 'light':
      changeThemeModeBtn.innerHTML = '<span><i class="fa-solid fa-lightbulb"></i></span>'
      return
    case 'dark':
      changeThemeModeBtn.innerHTML = '<span><i class="fa-solid fa-moon"></i></span>'
      return
    default:
      changeThemeModeBtn.innerHTML = '<span><i class="fa-solid fa-circle-half-stroke"></i></span>'
  }
}
updateChangeThemeModeBtn()

changeThemeModeBtn.onclick = () => {
  switch (themeMode) {
    case 'light':
      themeMode = 'dark'
      break
    case 'dark':
      themeMode = 'auto'
      break
    default:
      themeMode = 'light'
  }
  localStorage.setItem('theme', themeMode)
  applyTheme()
  updateChangeThemeModeBtn()
}
