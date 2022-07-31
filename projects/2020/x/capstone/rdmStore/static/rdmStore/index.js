document.addEventListener('DOMContentLoaded', function() {
    const sidebar = document.querySelector('#sidebar-div')
    if (sidebar) {
        sidebar.style.display = 'none'
    }
    const filtrarBtn = document.querySelector('#sidebar-btn')
    if (filtrarBtn) {
        filtrarBtn.addEventListener('click', function onClick() {
            if (sidebar.style.display === 'none') {
                sidebar.style.display = 'block'
            } else if (sidebar.style.display === 'block') {
                sidebar.style.display = 'none'
            }
        })
    }

    //const userId = document.querySelector('#hide').textContent
    //const navPages = document.querySelector('#nav-pages')
    //document.querySelector('#hide').style.display = 'none'
})

