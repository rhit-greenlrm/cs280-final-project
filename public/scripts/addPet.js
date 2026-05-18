

document.addEventListener("DOMContentLoaded", function(){
   document.getElementById(newPetForm).onsubmit(function(profile, filepath){
        //add new pet to database
        dataservice.add_animal(profile, filepath); 

        //TODO send to employee dashboard
    });   
});



