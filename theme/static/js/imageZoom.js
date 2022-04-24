images = document.querySelectorAll('article img')

for (image of images) {
    image.addEventListener('click', function () {
        if (this.classList[1] == 'clicked') {
            this.classList.remove('clicked')
        } else {
            this.classList.add('clicked')
        }
    })
}
