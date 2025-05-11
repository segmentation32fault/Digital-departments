function throttle(callee, timeout) {
    let timer = null

    return function perform(...args) {
        if (timer) return

        timer = setTimeout(() => {
            callee(...args)

            clearTimeout(timer)
            timer = null
        }, timeout)
    }
}

function checkPos()
{
    let height = document.body.offsetHeight
    let screenHeight = window.innerHeight

    const scrolled = window.scrollY
    const threshold = height - screenHeight / 4
    const position = scrolled + screenHeight

    if (position >= threshold) {
        //  подгружаем
    }
}


async function fetch_posts()
{
    const { posts, next } = await fetch()
}

;(() => {
    window.addEventListener('scroll', throttle(checkPos, 250))
    window.addEventListener('resize', throttle(checkPos, 250))
})()
