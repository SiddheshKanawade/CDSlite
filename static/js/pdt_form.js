function displaynext() {
    answer = document.getElementById("Merch").value;
    document.getElementById(answer).style.display = "block";

    if (answer == "Yes") { // hide the div that is not selected

        document.getElementById('No').style.display = "none";

    } else if (answer == "No") {

        document.getElementById('Yes').style.display = "none";

    }
}  
