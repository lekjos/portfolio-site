/**
   * Portfolio details slider
*/
// initialize swiper
 var portfolioSwiper = new Swiper('.portfolio-details-slider', {
    speed: 400,
    loop: true,
    autoplay: {
      delay: 5000,
      disableOnInteraction: true,
      pauseOnMouseEnter: true,
    },
    pagination: {
      el: '.swiper-pagination',
      type: 'bullets',
      clickable: true
    },
    navigation: {
      nextEl: '.swiper-button-next',
      prevEl: '.swiper-button-prev',  
    }
  });
  
  // find youtube player objects
  // from https://stackoverflow.com/questions/12522291/pausing-youtube-iframe-api-in-javascript
  var yt_int, yt_players={},
      initYT = function() {
          $(".embed > div > iframe").each(function() {
              yt_players[this.id] = new YT.Player(this.id);
          });
      };
  $.getScript("//www.youtube.com/player_api", function() {
      yt_int = setInterval(function(){
          if(typeof YT === "object"){
              initYT();
              clearInterval(yt_int);
          }
      },500);
  });

// pause embed when slide changes
var sliderVideos = $(".embed> div > iframe");

portfolioSwiper.on('slideChange', function () {
   sliderVideos.each(function( index ) {
     yt_players[this.id].stopVideo();
   });
});
