function openForm() {
    document.getElementById("login").style.display = "block";
  }
  function closeForm() {
    document.getElementById("login").style.display = "none";
  }

  // function createProductCards(products) {
  //   const productContainer = document.querySelector('.product_card');
  
  //   products.forEach(product => {
  //     const productCard = document.createElement('div');
  //     productCard.classList.add('product_card');
  
  //     const productImage = document.createElement('div');
  //     productCard.classList.add('product_card');
  //     productImage.classList.add('image');
  //     productCard.appendChild(productImage);
  
  //     const productName = document.createElement('div');
  //     productCard.classList.add('product_card');
  //     productCard.classList.add('details');
  //     productName.classList.add('card-name');
  //     productName.textContent = product.name;
  //     productCard.appendChild(productName);
  
  //     const productPrice = document.createElement('div');
  //     productCard.classList.add('product_card');
  //     productCard.classList.add('details');
  //     productPrice.classList.add('price');
  //     productPrice.textContent = product.price;
  //     productCard.appendChild(productPrice);
      
  //     productCard.classList.add('product_card');
  //     productContainer.appendChild(productCard);
  //   });
  // }

  function createProductCards(products) {
    const productContainer = document.querySelector('.product_container');
  
    for (let i = 0; i < products.length; i++) {
      const productCard = document.createElement('div');

      productCard.classList.add('product_card');

      const productImage = document.createElement('div');
      // productImage.classList.add('product_card');
      productImage.classList.add('image');
      const productImg = document.createElement('img');
      productImg.classList.add('card-img');
      productImg.src = products[i].imageUrl;
      productImg.alt = '';
      productImage.appendChild(productImg);
      productCard.appendChild(productImage);
  
      const productDetails = document.createElement('div');
      // productDetails.classList.add('product_card');
      productDetails.classList.add('details');
      const productLink = document.createElement('a');
      productLink.href = 'bid_buyer.html';
      const productName = document.createElement('h3');
      productName.classList.add('card-name');
      productName.textContent = products[i].name;
      productLink.appendChild(productName);
      productDetails.appendChild(productLink);
      const productPrice = document.createElement('span');
      productPrice.classList.add('price');
      productPrice.textContent = products[i].price;
      productDetails.appendChild(productPrice);
      // const proform = document.createElement('form');
      // proform.method = "POST";
      const productBid = document.createElement('a');
      // productBid.className="button_class"
      productBid.href = "/bid_buyer";
      const productButton = document.createElement('button');
      productButton.classList.add('buttons');
      
      productBid.textContent = 'Bid';
      productButton.appendChild(productBid);
      // proform.appendChild(productButton);
      productDetails.appendChild(productButton);
      productCard.appendChild(productDetails);
  
      productContainer.appendChild(productCard);
    }
  }
  