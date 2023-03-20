// const productImages = document.querySelectorAll("edit-img img"); 
// const productImageSlide = document.querySelector("card"); 

// let activeImageSlide = 0; 

// productImages.forEach((item, i) => { 
//     item.addEventListener('click', () => { 
//         productImages[activeImageSlide].classList.remove('active'); 
//         item.classList.add('active'); 
//         productImageSlide.style.backgroundImage = `url('${item.src}')`; 
//         activeImageSlide = i; 
//     })
// })

// const sizeBtns = document.querySelectorAll('.size_button'); 
// let checkedBtn = 0; 

// sizeBtns.forEach((item, i) => { 
//     item.addEventListener('click', () => { 
//         sizeBtns[checkedBtn].classList.remove('check'); 
//         item.classList.add('check'); 
//         checkedBtn = i; 
//     })
// })

function addToCart() {
    window.location.href = 'cart.html';
  }

  function myProducts(param1,param2) {
    var ans = confirm("Are you sure?")
    console.log(ans);
      if(ans){
        fetch(`/confirm_barter/${param1}/${param2}`)
        .then(response => response.text())
        .then(data => {
          console.log("in func")
          alert("Barter Succesfully Confirmed")
        })
        .catch(error => {
          console.log("here")
          console.error(error);
        });
      }
      else {
        alert("Barter Not Confirmed!")
      }
  }
  /*bid functions*/


  

  /* Barter_buyer Page*/

  function makeBarter_Buyer(productDetails){
    const DetailContainer = document.querySelector('.product-image');
    const br1 = document.createElement('br')
    const br2 = document.createElement('br')
    const br3 = document.createElement('br')
    const br4 = document.createElement('br')
    const br5 = document.createElement('br')
    const br6 = document.createElement('br')

    const imgsection = document.createElement('section');
    const imgdiv = document.createElement('div');
    imgdiv.classList.add('card');

    const imgdiv2 = document.createElement('div');
    imgdiv2.classList.add('edit-img');

    // const pimg = document.createElement('img');
    // pimg.src = productDetails.ImageUrl;
    // pimg.alt = "";

    DetailContainer.appendChild(imgsection);
    
    
    //imgdiv2.appendChild(pimg);
    imgdiv.appendChild(imgdiv2);
    imgsection.appendChild(imgdiv);

    const detailssec = document.createElement('section');

    const productNameElement = document.createElement('h1');
    productNameElement.textContent = productDetails['ProductName'];

    const productDetailsElement = document.createElement('p');
    productDetailsElement.classList.add('details');
    productDetailsElement.textContent = productDetails.Description_;
    

    const customerNameElement = document.createElement('p');
    customerNameElement.classList.add('details1');
    customerNameElement.textContent ="Name: " +  productDetails.Seller_Name;
    

    const customerEmailElement = document.createElement('p');
    customerEmailElement.classList.add('details1');
    customerEmailElement.textContent ="Email: " +  productDetails.Email_ID;
    

    const customerMobileElement = document.createElement('p');
    customerMobileElement.classList.add('details1');
    customerMobileElement.textContent ="Mobile: " +  productDetails.MobileNo;
    
    const confirmbutton = document.createElement('button');
    confirmbutton.classList.add('btns');
    confirmbutton.textContent = "Confirm";
    confirmbutton.addEventListener("click",function() {myProducts(productDetails['BarterID'], productDetails['ProductID']) });
    

    detailssec.appendChild(productNameElement);
    detailssec.appendChild(br1)
    detailssec.appendChild(br2)
    detailssec.appendChild(productDetailsElement);
    detailssec.appendChild(br3)
    detailssec.appendChild(customerNameElement);
    detailssec.appendChild(br4)
    detailssec.appendChild(customerEmailElement);
    detailssec.appendChild(br5)
    detailssec.appendChild(customerMobileElement);
    detailssec.appendChild(br6)
    detailssec.appendChild(confirmbutton);
    DetailContainer.appendChild(detailssec);


  }

function goToBarter_buyer(){

    window.location.href='barter_buyer.html';
  
  }