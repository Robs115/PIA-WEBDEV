

/* Esta funcion es inutil ahora:
function login(){
    let usuarios = ["Francisco", "Roberto", "Nelson"]
    let contrasenas = ["12345", "hamburguesa16", "contraseñaImposibleDeDescifrar"]

    let usuario = document.getElementById("txtUsuario").value;
    let contrasena = document.getElementById("txtContrasena").value;

    if ((usuarios.includes(usuario)) && (contrasenas.includes(contrasena))) {
        window.location.href = "/listar/";
    }
    else if (usuario == "kingEmperor" && contrasena == "bigGuy"){
        sessionStorage.setItem("kingEmperor", "bigGuy");
        window.location.href = "/listar/";
    }

    else {
        alert("That wont do");
    }
    
} */