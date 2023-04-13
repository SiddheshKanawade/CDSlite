

function createProductCards(products) {
    const productContainer = document.querySelector('.product_container');
  
    for (let i = 0; i < products.length; i++) {
      const productCard = document.createElement('div');

      productCard.classList.add('product_card');

      const productImage = document.createElement('div');
      //productImage.classList.add('product_card');
      productImage.classList.add('image');
      const productImg = document.createElement('img');
      productImg.classList.add('card-img');
      productImg.src = `/get_image/${products[i].ProductID}`;
      productImg.alt = '';
      productImage.appendChild(productImg);
      productCard.appendChild(productImage);
  
      var var1 = products[i]['ProductID'];
      var1 = JSON.parse(var1)
      const productDetails = document.createElement('div');
      //productDetails.classList.add('product_card');
      productDetails.classList.add('details');
      const productLink = document.createElement('a');
      productLink.href = `/in_merch/${var1}`;
      const productName = document.createElement('h3');
      productName.classList.add('card-name');
      productName.textContent = products[i]['ProductName'];
      productLink.appendChild(productName);
      productDetails.appendChild(productLink);
      const productPrice = document.createElement('span');
      productPrice.classList.add('price');
      productPrice.textContent = products[i]['MRP'];
      productDetails.appendChild(productPrice);
      const productBid = document.createElement('a');
      //productBid.className="button_class"
      
      productBid.href = `/add_cart/${var1}`;
      productBid.innerText = "Add to Cart";
      const productButton = document.createElement('button');
      productButton.classList.add('buttons');
      productButton.append(productBid);
      productDetails.appendChild(productButton);
      productCard.appendChild(productDetails);
      productContainer.appendChild(productCard);
    }
  }