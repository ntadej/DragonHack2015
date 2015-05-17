  var videoTag = document.createElement('script');

  videoTag.src = "https://www.youtube.com/iframe_api";
  var firstScriptTag = document.getElementsByTagName('script')[0];
  firstScriptTag.parentNode.insertBefore(videoTag, firstScriptTag);

  var player;
  /*function onYouTubeIframeAPIReady() {
    
  }*/

  function initPlayer() {
    player = new YT.Player('player', {
      height: '100%',
      width: '100%',
      // videoId: '',
      // events: {
      //   'onReady': onPlayerReady,
      //   'onStateChange': onPlayerStateChange
      // }
    });
  }

  function togglePause() {
    if (player.getPlayerState() == 2 || player.getPlayerState() == 0 || player.getPlayerState() == 5) {
      player.playVideo();
    } else {
      player.pauseVideo();
    }
  }