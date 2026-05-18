

document.addEventListener("DOMContentLoaded", function(){
    
    document.getElementById("newPetForm").addEventListener("submit", function(){
           //add new pet to database
           dataservice.add_animal(profile, filepath); 

          //send back to employee dashboard
          window.location.href = "./dashboard.html";
    });

});



