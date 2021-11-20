//dogs are cute and funny

window.addEventListener('load', () =>{
    const canvas = document.querySelector("#canvas");
    const context = canvas.getContext("2d");

    //sizing
    //canvas.setAttribute('width', canvas.parentNode.offsetWidth);
    //canvas.setAttribute('height', canvas.parentNode.offsetHeight);

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
        context.lineWidth = 10;
        context.lineCap = 'round';
        context.strokeStyle = 'black';

        context.lineTo(e.clientX, e.clientY);
        context.stroke();
        context.beginPath();
        context.moveTo(e.clientX, e.clientY);
    }

    canvas.addEventListener("mousedown", startPos);
    canvas.addEventListener("mouseup", endPos);
    canvas.addEventListener("mousemove", draw);

});

function Refresh() {
    const canvas = document.querySelector("#canvas");
    const context = canvas.getContext("2d");
    context.clearRect(0,0, canvas.width, canvas.height);
}