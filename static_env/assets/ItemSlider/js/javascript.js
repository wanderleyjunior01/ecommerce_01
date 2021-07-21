(function(win,doc){
    "use strict"
    if(doc.querySelector(".btnDel")){
        let btnDel = doc.querySelectorAll(".btnDel");
        for(let i=0; i < btnDel.length; i++){
            btnDel[i].addEventListener("click", function(event){
                if(confirm("Want to delete this product?")){
                    return true;
                }else{
                    event.preventDefault();
                }
            });
        }
    }  

    // Ajax for modal in edit products data

    if(doc.querySelector(".edit-form")){
        let form = doc.querySelector(".edit-form");
        let prodId = doc.querySelector("#prod-id")
        function getDataById(event)
        {
            event.preventDefault();
            let data = new ProductInfo.query.filter_by(id=prodId);
            let ajax = new XMLHttpRequest();
            ajax.open("POST");
            ajax.onreadystatechange = function()
            {
                if(ajax.status === 200 && ajax.readyState === 4){

                }
            }
            ajax.send(data)
        }
        form.addEventListener("click", getDataById, false);
    }

    // Ajax for Add Product

    if(doc.querySelector(".form")){
        let form2 = doc.querySelector(".form");
        console.log(form2 );
    }
}) (window,document);