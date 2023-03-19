function barterpage(){
    window.location.href = "barterpage.html";
}


const productImages = document.querySelectorAll("edit-img img"); 
const productImageSlide = document.querySelector("card"); 

let activeImageSlide = 0; 

productImages.forEach((item, i) => { 
    item.addEventListener('click', () => { 
        productImages[activeImageSlide].classList.remove('active'); 
        item.classList.add('active'); 
        productImageSlide.style.backgroundImage = `url('${item.src}')`; 
        activeImageSlide = i; 
    })
})

const sizeBtns = document.querySelectorAll('.size_button'); 
let checkedBtn = 0; 

sizeBtns.forEach((item, i) => { 
    item.addEventListener('click', () => { 
        sizeBtns[checkedBtn].classList.remove('check'); 
        item.classList.add('check'); 
        checkedBtn = i; 
    })
})