  var videoTag = document.createElement('script');

  videoTag.src = "https://www.youtube.com/iframe_api";
  var firstScriptTag = document.getElementsByTagName('script')[0];
  firstScriptTag.parentNode.insertBefore(videoTag, firstScriptTag);

  var player = null;
  var playerReady = false;
  /*function onYouTubeIframeAPIReady() {
    
  }*/

  function initPlayer(id) {
    player = new YT.Player('player', {
      height: '100%',
      width: '100%',
      videoId: id,
      events: {
        'onReady': onPlayerReady
      }
    });
  }

  function onPlayerReady() {
    player.playVideo();
    playerReady = true;
  }

  function togglePause() {
    if (!player || !playerReady) return;

    if (player.getPlayerState() == 2 || player.getPlayerState() == 0 || player.getPlayerState() == 5) {
      player.playVideo();
    } else {
      player.pauseVideo();
    }
  }