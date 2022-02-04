window.addEventListener('load', () =>{
    var canvas = document.querySelector("#canvas");
    var context = canvas.getContext("2d");
    //sizing
    var width = canvas.parentNode.offsetWidth;
    canvas.setAttribute('width', width - 10);
    canvas.setAttribute('height', width*1.294 - 10);

    context.fillStyle = "white";
    context.fillRect(0, 0, canvas.width, canvas.height);

    var rect = canvas.getBoundingClientRect();

    let painting = false;

    function startPos(e) {
        painting = true;
        draw(e);
    }
    function endPos() {
        painting = false;
        context.beginPath()
    }
    function draw(e) {
        if (!painting) return;
        context.lineWidth = 5;
        context.lineCap = 'round';
        context.strokeStyle = 'black';

        context.lineTo(e.clientX - rect.left - 5, e.clientY - rect.top - 8);
        context.stroke();
        context.beginPath();
        context.moveTo(e.clientX - rect.left - 5, e.clientY - rect.top - 8);
    }

    canvas.addEventListener("mousedown", startPos);
    canvas.addEventListener("mouseup", endPos);
    canvas.addEventListener("mousemove", draw);
    canvas.addEventListener("mouseout", endPos);

});

//Function run on click of Clear button. Clears the canvas rectangle and refills the white background
function Clear() {
    var canvas = document.querySelector("#canvas");
    var context = canvas.getContext("2d");

    context.clearRect(0, 0, canvas.width, canvas.height);

    context.fillStyle = "white";
    context.fillRect(0, 0, canvas.width, canvas.height);
}

//Function run on click of Submit button. Automatically downloads the canvas content as a png file, then clears the canvas rectangle and refills the white background
function Submit() {
    var canvas = document.querySelector("#canvas");
    var context = canvas.getContext("2d");
    
    /*var img = document.createElement('a');
    img.download = 'download.png';
    img.href = canvas.toDataURL("image/png");
    img.click();
    img.delete;*/

    var url = "http://127.0.0.1:8000/submit";

    var dataURL = canvas.toDataURL();

    $.ajax({
        type: "POST",
        url: url,
        data: {
            imageBase64: dataURL
        }
    });

    context.clearRect(0, 0, canvas.width, canvas.height);

    context.fillStyle = "white";
    context.fillRect(0, 0, canvas.width, canvas.height);
}
// Get the modal
var modal = document.getElementById("myModal");

// Get the image and insert it inside the modal - use its "alt" text as a caption
var img = document.getElementById("disneyImage");
var modalImg = document.getElementById("img01");
var captionText = document.getElementById("caption");
img.onclick = function(){
  modal.style.display = "block";
  modalImg.src = this.src;
  captionText.innerHTML = this.alt;
}

// Get the <span> element that closes the modal
var span = document.getElementsByClassName("close")[0];

// When the user clicks on <span> (x), close the modal
span.onclick = function() { 
  modal.style.display = "none";
}