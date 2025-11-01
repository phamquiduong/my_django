var themeMode = localStorage.getItem('theme') || 'auto'

const prefersDark = window.matchMedia('(prefers-color-scheme: dark)')
let prefersDarkListener = null

const changeTheme = (theme) => {
  document.documentElement.setAttribute('data-bs-theme', theme)
}

const applyTheme = () => {
  if (prefersDarkListener) {
    prefersDark.removeEventListener('change', prefersDarkListener)
    prefersDarkListener = null
  }

  if (themeMode === 'auto') {
    changeTheme(prefersDark.matches ? 'dark' : 'light')
    prefersDarkListener = (e) => changeTheme(e.matches ? 'dark' : 'light')
    prefersDark.addEventListener('change', prefersDarkListener)
  } else {
    changeTheme(themeMode)
  }
}

applyTheme()
