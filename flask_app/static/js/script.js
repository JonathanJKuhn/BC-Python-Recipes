var reg = document.getElementById("regpassword")
var con = document.getElementById("conpassword")
var log = document.getElementById("logpassword")
var show = document.getElementsByName("showpass")

function toggleShowPassword() {

    if (reg.type === "password") {
        reg.type = "text"
        con.type = "text"
        log.type = "text"
        show.forEach( e => {
            e.checked = true
            }
        )
    } else {
        reg.type = "password"
        con.type = "password"
        log.type = "password"
        show.forEach( e => {
            e.checked = false
            }
        )
    }
}

show.forEach(e => {
    e.addEventListener("click", toggleShowPassword)
    }
)