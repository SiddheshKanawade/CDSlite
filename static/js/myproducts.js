
function createProductCards(products, type) {
  if(type == 'vp'){
    console.log(products)
    const productContainer = document.querySelector('.product_container');
  
    for (let i = 0; i < products.length; i++) {
      const productCard = document.createElement('div');

      productCard.classList.add('product_card');

      // const productImage = document.createElement('div');
      // // productImage.classList.add('product_card');
      // productImage.classList.add('image');
      // const productImg = document.createElement('img');
      // productImg.classList.add('card-img');
      // productImg.src = products[i].imageUrl;
      // productImg.alt = '';
      // productImage.appendChild(productImg);
      // productCard.appendChild(productImage);
  
      const productDetails = document.createElement('div');
      var var1 = products[i]['ProductID'];
      var1 = JSON.parse(var1);
      console.log(var1)
      // productDetails.classList.add('product_card');
      productDetails.classList.add('details');
      const productLink = document.createElement('a');
      productLink.href = `/bid_page/${var1}`;
      const productName = document.createElement('h3');
      productName.classList.add('card-name');
      productName.textContent = products[i].ProductName;
      productLink.appendChild(productName);
      productDetails.appendChild(productLink);
      const productPrice = document.createElement('span');
      productPrice.classList.add('price');
      productPrice.textContent = "Rs. " + products[i].BasePrice;
      productDetails.appendChild(productPrice);
      const product_A = document.createElement('a');
      product_A.classList.add("button_class");
      const productBid = document.createElement('a');
      productBid.className="button_correct"
      
      productBid.href =  `/vp_products/${var1}`;
      const productButton = document.createElement('button');
      productButton.classList.add('buttons');
      productBid.textContent = 'Edit';
      //productButton.addEventListener("click",editproduct);
      productButton.appendChild(productBid);
      const deleteButton = document.createElement('button');
      deleteButton.classList.add('buttons');
      deleteButton.textContent = 'Delete';
      deleteButton.addEventListener("click",function() { del_Function_vp(products[i].ProductID); });
      //productButton.appendChild(deleteButton);
      product_A.appendChild(productButton);
      product_A.appendChild(deleteButton);
      productDetails.appendChild(product_A);
      productCard.appendChild(productDetails);
  
      productContainer.appendChild(productCard);
    }
    }else{
      console.log(products)
      const productContainer = document.querySelector('.product_container');
  
      for (let i = 0; i < products.length; i++) {
        const productCard = document.createElement('div');

        productCard.classList.add('product_card');

        // const productImage = document.createElement('div');
        // // productImage.classList.add('product_card');
        // productImage.classList.add('image');
        // const productImg = document.createElement('img');
        // productImg.classList.add('card-img');
        // productImg.src = products[i].imageUrl;
        // productImg.alt = '';
        // productImage.appendChild(productImg);
        // productCard.appendChild(productImage);
    
        const productDetails = document.createElement('div');
        // productDetails.classList.add('product_card');
        productDetails.classList.add('details');
        const productLink = document.createElement('a');
        productLink.href = '#';
        const productName = document.createElement('h3');
        productName.classList.add('card-name');
        productName.textContent = products[i].ProductName;
        productLink.appendChild(productName);
        productDetails.appendChild(productLink);
        const productPrice = document.createElement('span');
        productPrice.classList.add('price');
        productPrice.textContent = "Rs. " + products[i].MRP;
        productDetails.appendChild(productPrice);
        const product_A = document.createElement('a');
        product_A.classList.add("button_class");
        const productBid = document.createElement('a');
        productBid.className="button_correct"
        var var1 = products[i]['ProductID'];
        var1 = JSON.parse(var1);
        console.log(var1)
        productBid.href =  `/fp_products/${var1}`;
        const productButton = document.createElement('button');
        productButton.classList.add('buttons');
        productBid.textContent = 'Edit';
        //productButton.addEventListener("click",editproduct);
        productButton.appendChild(productBid);
        const deleteButton = document.createElement('button');
        deleteButton.classList.add('buttons');
        deleteButton.textContent = 'Delete';
        deleteButton.addEventListener("click",function() { del_Function_fp(products[i].ProductID); });
        //productButton.appendChild(deleteButton);
        product_A.appendChild(productButton);
        product_A.appendChild(deleteButton);
        productDetails.appendChild(product_A);
        productCard.appendChild(productDetails);
    
        productContainer.appendChild(productCard);
      }
  }
}
