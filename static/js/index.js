function createProductCards(products) {
  //console.log(products)
  const productContainer = document.querySelector('.product_container');
  //const ImgUrls = [{ imageUrl: "hoodie.png" }, { imageUrl: "fridge.jpeg" }, { imageUrl: "product1.png" }, { imageUrl: "product2.png" }, { imageUrl: "bat.jpeg" },
  //{ imageUrl: "jacket.jpg" }, { imageUrl: "Sweater.jpeg" }, { imageUrl: "racket.jpeg" }]

  for (let i = 0; i < products.length; i++) {
    if(products[i].isBarter=="Yes"){
      const productCard = document.createElement('div');
      productCard.classList.add('product_card');
  
      const productImage = document.createElement('div');
      productImage.classList.add('image');
  
      const productImg = document.createElement('img');
      productImg.classList.add('card-img');
      productImg.src = `/get_image/${products[i].ProductID}`;
      productImg.alt = '';
  
      productImage.appendChild(productImg);
      productCard.appendChild(productImage);
  
      const productDetails = document.createElement('div');
      productDetails.classList.add('details');
      var var1 = products[i]['ProductID'];
      var1 = JSON.parse(var1)
  
      const productLink = document.createElement('a');
      productLink.href = `/bid_buyer/${var1}`;
  
      const productName = document.createElement('h3');
      productName.classList.add('card-name');
      productName.textContent = products[i].ProductName;
  
      productLink.appendChild(productName);
      productDetails.appendChild(productLink);
  
      const productPrice = document.createElement('span');
      productPrice.classList.add('price');
      productPrice.textContent = "Rs. " + products[i].BasePrice;
  
      productDetails.appendChild(productPrice);
  
      const productButtons = document.createElement('div');
      productButtons.classList.add("buttons_space")
      const Button1 = document.createElement('button');
      Button1.classList.add('buttons');
  
      const productBid = document.createElement('a');
      productBid.href = `/bid_buyer/${var1}`;
      productBid.textContent = 'Bid';

      Button1.appendChild(productBid);

      const Button2 = document.createElement('button');
      Button2.classList.add('buttons');
  
      const productBarter = document.createElement('a');
      productBarter.href = `/bid_buyer/${var1}`;
      productBarter.textContent = 'Barter';  

      Button2.appendChild(productBarter);

      productButtons.appendChild(Button1);
      productButtons.appendChild(Button2);
      productDetails.appendChild(productButtons)
      productCard.appendChild(productDetails);
      productContainer.appendChild(productCard);
    }
    else{
      const productCard = document.createElement('div');
      productCard.classList.add('product_card');
  
      const productImage = document.createElement('div');
      productImage.classList.add('image');
  
      const productImg = document.createElement('img');
      productImg.classList.add('card-img');
      productImg.src = `/get_image/${products[i].ProductID}`;
      productImg.alt = '';
  
      productImage.appendChild(productImg);
      productCard.appendChild(productImage);
  
      const productDetails = document.createElement('div');
      productDetails.classList.add('details');
      var var1 = products[i]['ProductID'];
      var1 = JSON.parse(var1)
  
      const productLink = document.createElement('a');
      productLink.href = `/bid_buyer/${var1}`;
  
      const productName = document.createElement('h3');
      productName.classList.add('card-name');
      productName.textContent = products[i].ProductName;
  
      productLink.appendChild(productName);
      productDetails.appendChild(productLink);
  
      const productPrice = document.createElement('span');
      productPrice.classList.add('price');
      productPrice.textContent = "Rs. " + products[i].BasePrice;
  
      productDetails.appendChild(productPrice);
  
      const productButton = document.createElement('button');
      productButton.classList.add('buttons');
  
      const productBid = document.createElement('a');
      productBid.href = `/bid_buyer/${var1}`;
      productBid.textContent = 'Bid';
  
      productButton.appendChild(productBid);
      productDetails.appendChild(productButton);
      productCard.appendChild(productDetails);
      productContainer.appendChild(productCard);
    }
  }
}
