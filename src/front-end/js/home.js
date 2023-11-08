var home = "MIRROR";
    var speeds = 750;

    var j = 0;

    function autoTypers() {
        document.getElementById("hometext").innerHTML += home.charAt(j);
        j++;

        setTimeout(autoTypers, speeds);
    }

    autoTypers();