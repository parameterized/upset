window.pyscriptLoaded = False;
window.gol = null;
window.golRenderer = null;
window.simImg = null

function setup() {
    createCanvas(innerWidth, innerHeight).parent("sketch");
}

function pyscriptSetup() {
    pyscriptLoaded = true;
    let pg = pyscript.interpreter.globals;
    gol = pg.get("GOL")(64);
    golRenderer = pg.get("CellRenderer")(gol);
    simImg = createGraphics(640, 640);
    simImg.loadPixels();
}

function copyPixels(src) {
    // https://forum.processing.org/two/discussion/10485/troubles-with-the-p5-image-pixels-array
    const args = arguments.length;
    var sIdx = 0, dst = arguments[1], dIdx = 0,
        len = args == 3 ? ~~Math.abs(arguments[2]) : src.length;
    if (args > 3) {
        sIdx = ~~Math.abs(dst);
        dst = arguments[2];
        dIdx = ~~Math.abs(arguments[3]);
        len = args > 4 ? ~~Math.abs(arguments[4]) : len;
    }
    const sLen = src.length, dLen = dst.length, end = Math.min(len + sIdx, sLen);
    if (!sIdx && sLen <= len && sLen + dIdx <= dLen && ArrayBuffer.isView(dst))
        dst.set(src, dIdx);
    else
        for (var i = sIdx, j = dIdx; i < end & j < dLen; dst[j++] = src[i++]);
    return dst;
}

function draw() {
    if (!window.pyscriptLoaded) {
        return;
    }
    background(230);
    copyPixels(golRenderer.render(), window.simImg.pixels);
    window.simImg.updatePixels();
    image(window.simImg, 0, 0);

    gol.step();
}