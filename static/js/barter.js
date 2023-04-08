function openForm() {
    document.getElementById("login").style.display = "block";
  }
  function closeForm() {
    document.getElementById("login").style.display = "none";
  }

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
      productImg.src = `/get_image/${products[i].ProductID}`;
      productImg.alt = '';
      productImage.appendChild(productImg);
      productCard.appendChild(productImage);
  
      const productDetails = document.createElement('div');
      // productDetails.classList.add('product_card');
      productDetails.classList.add('details');
      const productLink = document.createElement('a');
      productLink.href = 'barterproduct.html';
      const productName = document.createElement('h3');
      productName.classList.add('card-name');
      productName.textContent = products[i].name;
      productLink.appendChild(productName);
      productDetails.appendChild(productLink);
      const productPrice = document.createElement('span');
      productPrice.classList.add('price');
      productPrice.textContent = products[i].price;
      productDetails.appendChild(productPrice);
      const productBid = document.createElement('a');
      productBid.className="button_class"
      productBid.href = 'barterpage.html';
      const productButton = document.createElement('button');
      productButton.classList.add('buttons');
      productButton.textContent = 'Barter';
      productBid.appendChild(productButton);
      productDetails.appendChild(productBid);
      productCard.appendChild(productDetails);
  
      productContainer.appendChild(productCard);
    }
  }
  