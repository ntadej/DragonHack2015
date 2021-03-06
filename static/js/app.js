var animationDuration = 300;

var measuringProgress = 0;

var bpmStream = new EventSource('/bpm');
var maxMove = 0;
var lastBlink = 0;
var jawCount = 0;

var moveCallback = function(e)
{
	if (!$('#measuring:visible').length) {
		return;
	}

	var m = Math.abs(e.data);
	if (m > maxMove) {
		maxMove = m;
	}

	var ratio = e.data / (2 * maxMove) + 0.5;
	var size = $('#measuring .movement-wrapper').width() * ratio;

	$('#measuring .movement').css('width', size).css('height', size).css('margin-top', -size/2);
};

var calculatedCallback = function(e)
{
	if ($('#instructions:visible').length) {
		return;
	}

    console.log(e.type, e.data);

    var data = JSON.parse(e.data);

    $('#bpm').text(data.bpm);

	$('#song').text(data.song);
	$('#itunes').attr('href', data.itunes_link);

    //bpmStream.removeEventListener('move', moveCallback, false);
	bpmStream.removeEventListener('calculated', calculatedCallback, false);

	$('#measuring').fadeOut(animationDuration, function() {
		$('#result').fadeIn(animationDuration, function()
		{
		    if (player) {
				player.loadVideoById(data.yt_id);
			} else {
				initPlayer(data.yt_id);
			}
		});
		jawCount = 0;
		$('#result .progress').width(0);
	});
};

bpmStream.addEventListener('move', moveCallback, false);

// var headCallback = function(e)
// {
// 	if (!$('#result:visible').length) {
// 		return;
// 	}

//     console.log(e.type, e.data);

//     $.get('/getnext?bpm=' + $('#bpm').text(), function(response) {
//     	calculatedCallback({ type: 'complete', data: response });
//     });
// };

var jawCallback = function(e)
{
	if ($('#measuring:visible').length) {
		return;
	}

    console.log(e.type, e.data);

    if (jawCount > 10) {
    	return;
    }

    jawCount += 1;

	var progress;
	if ($('#instructions:visible').length) {
		progress = $('#instructions .progress');
	} else {
		progress = $('#result .progress');
	}

	progress.show();
    progress.css('width', 100 * jawCount / 10 + '%');

    if (jawCount == 10) {
    	if ($('#instructions:visible').length) {
    		$.get('/restart', startMeasuring);
    	} else if ($('#result:visible').length) {
    		$.get('/restart', startMeasuring);
    	}
    }
};

var blinkCallback = function(e)
{
	if ($('#instructions:visible').length || $('#measuring:visible').length) {
		return;
	}

    console.log(e.type, e.data);

    if (e.data - lastBlink < 0.4) {
    	togglePause();
    	lastBlink = 0;
    } else {
    	lastBlink = e.data;
    }
};

var statusCallback = function(e)
{
	if (!$('#instructions:visible').length) {
		return;
	}

	var data = JSON.parse(e.data);
	var items = $('.status-item');

	for (var i = 0; i < items.length; i++) {
		$(items[i]).css('background', data[i] == 1 ? 'green' : 'red');
	}
};

var statusStream = new EventSource('/status');
statusStream.addEventListener('status', statusCallback, false);

// var headStream = new EventSource('/headswipe');
// headStream.addEventListener('head', headCallback, false);

var jawStream = new EventSource('/jaw');
jawStream.addEventListener('jawclench', jawCallback, false);

var blinkStream = new EventSource('/blink');
blinkStream.addEventListener('blink', blinkCallback, false);

$('document').ready(function () {
	$('#instructions').fadeIn(animationDuration);
});

var updateMeasuringProgress = function()
{
	var diff = new Date().getTime() - measuringProgress;

	$('#measuring .progress').show();
	$('#measuring .progress').css('width', 100 * diff / (6 * 1000) + '%');

	if (diff < 6 * 1000) {
		window.setTimeout(updateMeasuringProgress, 20);
	}
};

var startMeasuring = function()
{
	var current;
	if ($('#instructions:visible').length) {
		current = '#instructions';
	} else {
		current = '#result';
	}

	if (player) {
		player.destroy();
		player = null;
	}

	$(current).fadeOut(animationDuration, function() {
		bpmStream.addEventListener('calculated', calculatedCallback, false);

		$('#measuring').fadeIn(animationDuration);
		$('#measuring .movement-wrapper').height($('#measuring .movement-wrapper').width());
		$('#measuring .movement').height($('#measuring .movement-wrapper').width());
	});

	measuringProgress = new Date().getTime();
	window.setTimeout(updateMeasuringProgress, 20);
};
