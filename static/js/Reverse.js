// HelloPixel.js
function start() {
    var canvas = document.getElementById('canvas');
    var context = canvas.getContext('2d');

    var image = new Image();
    image.onload = function() {
        context.drawImage(image, 0, 0);
        var imageData = context.getImageData(0, 0, image.width, image.height);
        var length = imageData.data.length;
        var pixel = imageData.data;
        for(var i = 0; i < length; i += 4) {
            pixel[i + 0] = 255 - pixel[i + 0];
            pixel[i + 1] = 255 - pixel[i + 1];
            pixel[i + 2] = 255 - pixel[i + 2];
        }
        context.putImageData(imageData, 0, 0);
    };
    image.src = 'static/img/Mario_png.png';
}
