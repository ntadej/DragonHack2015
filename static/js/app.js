var bpmStream = new EventSource('/bpm');

var moveCallback = function(e)
{
    console.log(e.type, e.data);
};

var calculatedCallback = function(e)
{
    console.log(e.type, e.data);

    bpmStream.removeEventListener('move', moveCallback, false);
	bpmStream.removeEventListener('calculated', calculatedCallback, false);
};

var restartCallback = function(e)
{
    console.log(e.type, e.data);
};

var testCallback = function(e)
{
    console.log(e.type, e.data);
};

bpmStream.addEventListener('move', moveCallback, false);
bpmStream.addEventListener('calculated', calculatedCallback, false);
bpmStream.addEventListener('restart', restartCallback, false);
bpmStream.addEventListener('test', testCallback, false);

window.addEventListener("beforeunload", function (event) {
    bpmStream.close();
});