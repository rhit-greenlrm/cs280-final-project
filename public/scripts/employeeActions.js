/*employee only TODOS
* banner link functionality
* displaying all images in database
* button functionality for scrolling photos
* displaying pet data alongside correct photo
*/
document.addEventListener("DOMContentLoaded", function(){
    document.getElementById("add").addEventListener("click", function(){
        window.location.href = "./add_pet.html";
    });

    document.getElementById("remove").addEventListener("click", function(){
        //remove pet from db and refresh display
    });

    document.getElementById("leftScroll").addEventListener("click", function(){
        //left scroll in photo display
    });

    document.getElementById("rightScroll").addEventListener("click", function(){
        //right scroll in photo display
    });

});


