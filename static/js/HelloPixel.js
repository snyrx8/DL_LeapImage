// HelloPixel.js
function start() {
    var canvas = document.getElementById('canvas');
    var context = canvas.getContext('2d');

    var image = new Image();
    image.onload = function() {
        context.drawImage(image, 0, 0);
        var imageData = context.getImageData(0, 0, image.width, image.height);
        console.log(imageData.data[0], imageData.data[1], imageData.data[2], imageData.data[3]);
    };
    image.src = 'static/img/Mario_png.png';
}
