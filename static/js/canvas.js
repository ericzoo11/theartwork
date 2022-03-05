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

//Function run on click of Clear Current button. Clears the Current Submissions image
function Current() {
    var url = "http://127.0.0.1:8000/clear";
    
    $.ajax({
        type: "POST",
        url: url,
    });

    var timeStamp = new Date().getTime();

    var curr = document.getElementById("myImg4");
    var currSrc = curr.src;

    curr.src = currSrc + '?t=' + timeStamp;
}

//Function run on click of Clear Current button. Clears the Current Submissions image
function Update() {
    var timeStamp = new Date().getTime();

    var curr = document.getElementById("myImg4");
    var currSrc = curr.src;

    curr.src = currSrc + '?t=' + timeStamp;
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
    
    var timeStamp = new Date().getTime();

    var curr = document.getElementById("myImg4");
    var currSrc = curr.src;

    curr.src = currSrc + '?t=' + timeStamp;
}

// Get the modal
var modal = document.getElementById("myModal");
var img = document.getElementById("myImg");
var modalImg = document.getElementById("img01");
var captionText = document.getElementById("caption");

document.addEventListener('click', function(e) {
    var targetId = e.target.id;
    //simple id filter
    if(targetId == "myImg" || targetId == "myImg1" || targetId == "myImg2" || targetId == "myImg3" || targetId == "myImg4"){
        img = document.getElementById(e.target.id);
        console.log("img")
        modal.style.display = "block";
        modalImg.src = img.src;
        captionText.innerHTML = img.alt;
    }
}, false);





// Get the <span> element that closes the modal
var span = document.getElementsByClassName("close")[0];

// When the user clicks on <span> (x), close the modal
span.onclick = function() { 
  modal.style.display = "none";
}