function confirmBid(param1) 
{
  var ans = confirm("Are you Sure to confirm the Bid?");
  console.log(ans);
  if(ans) {
    fetch(`/confirm_bid/${param1}`)
    .then(response => response.text())
    .then(data => {
      console.log("in func");
      alert("Bid Confirmed Succesfully")
    })
    .catch(error => {
      console.log("here")
      console.error(error);
    });
  }
  else{
    alert("Bid Not Confirmed!")
  }
}


function displayBidsAsButtons(bidsArray) {
    const displayBids = document.querySelector('.Display_Bids');
    // Loop through the bids array and create a button for each bid
    
    for (let i = 0; i < bidsArray.length; i++) {
      // Create a new button element
      
      
      if(bidsArray[i].BidStatus == 'Confirmed')
      {
        const Bidbutton = document.createElement("button");
        Bidbutton.id = "bid_btn_id";
        Bidbutton.classList.add('btns');
        Bidbutton.addEventListener("click",function() {confirmBid(bidsArray[i].BidID);} );

  
      // Set the button text to the bid amount
        Bidbutton.innerText = "Bid "+(i+1)+": Rs. " + bidsArray[i]['BidPrice'];
        Bidbutton.style.color = "white";
        Bidbutton.style.backgroundColor = "green";
        Bidbutton.style.fontWeight = "bold";
      // Add the button to the HTML document
        displayBids.appendChild(Bidbutton);
        console.log(bidsArray[i].BidStatus,bidsArray[i].BidID )
      }
      else
      {
        const Bidbutton = document.createElement("button");
        Bidbutton.id = "bid_btn_id";
        Bidbutton.classList.add('btns');
        Bidbutton.addEventListener("click",function() {confirmBid(bidsArray[i].BidID);} );

    
        // Set the button text to the bid amount
        Bidbutton.innerText = "Bid "+(i+1)+": Rs. " + bidsArray[i]['BidPrice'];
    
        // Add the button to the HTML document
        displayBids.appendChild(Bidbutton);
    }
    // document.body.appendChild(displayBids);
  }
}

function goToBarter_buyer(){

    window.location.href='barter_buyer.html';
  
  }

function displayBarterAsButtons(BarterArray) {
    const displayBarter = document.querySelector('.Display_Bids');
    // Loop through the bids array and create a button for each bid
    for (let i = 0; i < BarterArray.length; i++) {
      // Create a new button element
      
      const Barterbutton = document.createElement("button");
      Barterbutton.id = "bid_btn_id";
      Barterbutton.classList.add('btns1');
      // Set the button text to the bid amount
      const elm = document.createElement("a");
      const var1 = BarterArray[i]['BarterID'];
      try {
        var1 = JSON.parse(var1);
      }
      catch (error) {
        console.log('Error parsing JSON:', error, var1);
      }
      console.log("var1 ", var1);
      elm.innerText = BarterArray[i].ProductName;
      elm.href = `/buyer_barter/${var1}`;
      Barterbutton.append(elm);
      //Barterbutton.addEventListener("click",function() {confirm_barter(BarterArray[i].BarterID);});
  
      if(BarterArray[i].BidStatus == 'Confirmed')
      {
        const bid_btn = document.getElementById("bid_btn_id");
        bid_btn.style.color = "white";
        bid_btn.style.backgroundColor = "green";
        bid_btn.style.fontWeight = "bold";
      }
      // Add the button to the HTML document
      displayBarter.appendChild(Barterbutton);
    }
    // document.body.appendChild(displayBids);

  }
