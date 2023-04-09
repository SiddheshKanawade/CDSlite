function displaynext() {
    answer = document.getElementById("Merch").value;
    document.getElementById(answer).style.display = "block";

    if (answer == "Yes") { // hide the div that is not selected

        document.getElementById('No').style.display = "none";

    } else if (answer == "No") {

        document.getElementById('Yes').style.display = "none";

    }
}  

function match_subcat(subcatlist, constrainlist) {
    cat_ID = document.getElementById("cat").value;

    const subs = []
    for (let i in constrainlist) {
        if(constrainlist[i].CategoryID == cat_ID) {
            subs.push(constrainlist[i].SubCategoryID);
        }
    }

    const sublist = []
    for (let i in subs) {
        for (let j in subcatlist) {
            if (subs[i] == subcatlist[j].SubcategoryID) {
                sublist.push(subcatlist[j]);
                break;
            }
        }
    }

    console.log("subcatlist: ", sublist);
    var select = document.getElementById("scat");

    select.innerHTML = '<option disabled selected value> -- select an option -- </option>';

    for(let i in sublist)
    {
        newOption = document.createElement('option');
        newOption.value=sublist[i].SubcategoryID;
        newOption.text=sublist[i].subcatName;
        select.appendChild(newOption);
    }

    
}