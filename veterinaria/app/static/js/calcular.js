function calculartotal() {
    let servicio = document.getElementById("ddlServicios").value;
    console.log(servicio)
    if (servicio == "1") {
        document.getElementById("calcularTotal").innerHTML = "total1";
    }
}