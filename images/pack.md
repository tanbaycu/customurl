<div class="slideshow-container">

  <div class="mySlides fade">
    <img src="https://i.postimg.cc/m2MwRyzC/image.png" style="width:100%">
  </div>

  <div class="mySlides fade">
    <img src="https://i.postimg.cc/cCtvRTym/image.png" style="width:100%">
  </div>

  <div class="mySlides fade">
    <img src="https://i.postimg.cc/ydbJ3t5x/image.png" style="width:100%">
  </div>

  <div class="mySlides fade">
    <img src="https://i.postimg.cc/Kzzkzx0C/07902851-B0-B7-4-D39-B6-C8-9-D73571-F42-A2.png" style="width:100%">
  </div>

</div>

<style>
  .slideshow-container {
    max-width: 1000px;
    position: relative;
    margin: auto;
  }

  .mySlides {
    display: none;
  }

  .fade {
    -webkit-animation-name: fade;
    -webkit-animation-duration: 1.5s;
    animation-name: fade;
    animation-duration: 1.5s;
  }

  @-webkit-keyframes fade {
    from {opacity: .4} 
    to {opacity: 1}
  }

  @keyframes fade {
    from {opacity: .4} 
    to {opacity: 1}
  }
</style>

<script>
  let slideIndex = 0;
  showSlides();

  function showSlides() {
    let i;
    let slides = document.getElementsByClassName("mySlides");
    for (i = 0; i < slides.length; i++) {
      slides[i].style.display = "none";  
    }
    slideIndex++;
    if (slideIndex > slides.length) {slideIndex = 1}    
    slides[slideIndex-1].style.display = "block";  
    setTimeout(showSlides, 2000); // Change image every 2 seconds
  }
</script>