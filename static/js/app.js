var bpmStream = new EventSource('/bpm');
var maxMove = 0;

var moveCallback = function(e)
{
	var m = Math.abs(e.data);
	if (m > maxMove) {
		maxMove = m;
	}

	$('#bpm').css('background', 'red');
	$('#bpm').css('opacity', e.data / (2 * maxMove) + 0.5);
};

var calculatedCallback = function(e)
{
    console.log(e.type, e.data);

    var data = JSON.parse(e.data);

    $('#bpm').text(data.bpm);
    
    if (player) {
    	player.loadVideoById(data.yt_id);
	}

	$('#song').text(data.song);
	$('#itunes').attr('href', data.itunes_link);

    //bpmStream.removeEventListener('move', moveCallback, false);
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