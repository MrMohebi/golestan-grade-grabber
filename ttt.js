function enterCaptcha() {
    if (window.location.host.match(/eduold\.uk\.ac\.ir/)) {
        var elementExistsInterval = setInterval(function () {
            if (
                document
                    .getElementById("Faci1")
                    ?.contentDocument?.getElementsByName?.("Master")?.[0]
                    ?.contentDocument?.getElementsByName?.("Form_Body")?.[0]
                    ?.contentDocument?.getElementById?.("imgCaptcha")
            ) {
                clearInterval(elementExistsInterval)
                let captchaImg = document
                    .getElementById("Faci1")
                    ?.contentDocument?.getElementsByName?.("Master")?.[0]
                    ?.contentDocument?.getElementsByName?.("Form_Body")?.[0]
                    ?.contentDocument?.getElementById?.("imgCaptcha")
                let captcha = captchaImg.src
                const toDataURL = url => fetch(url)
                    .then(response => response.blob())
                    .then(blob => new Promise((resolve, reject) => {
                        const reader = new FileReader()
                        reader.onloadend = () => resolve(reader.result)
                        reader.onerror = reject
                        reader.readAsDataURL(blob)
                    }))

                function solveCaptcha(src) {
                    toDataURL(src).then(dataUrl => {
                        const form = new FormData()
                        form.set("img", dataUrl.replace("data:image/gif;base64,", ""))

                        fetch("https://captcha.mdhi.dev/edu", {
                            method: "POST",
                            body: form,
                        })
                            .then(res => res.json())
                            .then(res => {
                                var box = document
                                    ?.getElementById?.("Faci1")
                                    ?.contentDocument?.getElementsByName?.("Master")?.[0]
                                    ?.contentDocument?.getElementsByName?.("Form_Body")?.[0]
                                    ?.contentDocument?.getElementById?.("F51701")
                                box.value = res.captcha || ""
                                // click login btn
                                document.getElementById("Faci1")?.contentDocument?.getElementsByName?.("Master")?.[0]?.contentDocument?.getElementsByName?.("Form_Body")?.[0]?.contentDocument?.getElementById?.("btnLog").click()
                            })
                            .catch(err => console.error(err))
                    })
                }

                solveCaptcha(captcha)

                observer = new MutationObserver(changes => {
                    changes.forEach(change => {
                        if (change.attributeName.includes("src")) {
                            if (captchaImg.src !== "https://eduold.uk.ac.ir/_images/webbusy.gif")
                                solveCaptcha(captchaImg.src)
                        }
                    })
                })
                observer.observe(captchaImg, {attributes: true})
            }
        }, 1000)
        setTimeout(function () {
            clearInterval(elementExistsInterval)
        }, 30000)
    }
}

enterCaptcha()

