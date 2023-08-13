window.pyscriptLoaded = False;
window.trees = null;
window.stepInterval = null;

function setup() {
    createCanvas(innerWidth, innerHeight).parent("sketch");
}

function pyscriptSetup() {
    pyscriptLoaded = true;
    let pg = pyscript.interpreter.globals;
    trees = pg.get("Trees")();

    stepInterval = setInterval(() => {
        trees.step();
    }, 1000 / 30);
}

function keyPressed() {
    if (keyCode == 32) { // Space
        clearInterval(stepInterval);
        pyscriptSetup();
    }
}

function draw() {
    if (!window.pyscriptLoaded) {
        return;
    }
    background(230);
    push();

    // Edges
    stroke(128);
    let treesScale = 30;
    strokeWeight(2 / treesScale);
    translate(200, 300);
    scale(treesScale);
    for (let e of trees.S_i.values()) {
        let parent = trees.S_i.get(e.parent_id);
        if (parent == undefined) {
            continue;
        }
        line(parent.x, -parent.y, e.x, -e.y);
    }
    // Nodes
    fill(0);
    noStroke();
    for (let e of trees.S_i.values()) {
        circle(e.x, -e.y, 5 / treesScale);
    }

    pop();
}