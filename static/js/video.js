  var videoTag = document.createElement('script');

  videoTag.src = "https://www.youtube.com/iframe_api";
  var firstScriptTag = document.getElementsByTagName('script')[0];
  firstScriptTag.parentNode.insertBefore(videoTag, firstScriptTag);

  var player;
  function onYouTubeIframeAPIReady() {
    player = new YT.Player('player', {
      height: '390',
      width: '640',
      // videoId: '',
      // events: {
      //   'onReady': onPlayerReady,
      //   'onStateChange': onPlayerStateChange
      // }
    });
  }