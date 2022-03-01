/**
   * Portfolio details slider
*/
 var portfolioSwiper = new Swiper('.portfolio-details-slider', {
    speed: 400,
    loop: true,
    autoplay: {
      delay: 5000,
      disableOnInteraction: true
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
  


var sliderVideos = $(".embed");
console.log('sliderVideos')
console.log(sliderVideos)
portfolioSwiper.on('slideChange', function () {
   sliderVideos.each(function( index ) {
     console.log('slide Change Triggered')
    this.currentTime = 0;
    this.pause();
   });
});