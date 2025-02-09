# 🚀 URL Shortener: A Full-Stack Web Application

Welcome to our cutting-edge URL Shortener application! This project demonstrates the power of combining modern frontend technologies with a robust backend to create a seamless user experience.

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

## 🌟 Features

- **URL Shortening**: Convert long URLs into short, manageable links
- **Custom Short Codes**: Create personalized short codes for your URLs
- **QR Code Generation**: Instantly generate QR codes for shortened URLs
- **History Tracking**: Keep track of your recently shortened URLs
- **Usage Statistics**: View click statistics for your shortened links
- **Responsive Design**: Seamlessly works on desktop and mobile devices
- **Dark Mode**: Toggle between light and dark themes for comfortable viewing
- **Pixel-Perfect UI**: Unique pixel-corner design for a retro-modern feel
- **Animations**: Smooth transitions and micro-interactions for enhanced UX

## 🛠️ Technology Stack

- **Frontend**: 
  - HTML5 
  - CSS3 (Tailwind CSS)
  - JavaScript (ES6+)
- **Backend**: 
  - Python 3.x
  - Flask framework
- **Database**: 
  - SQLite 
  - SQLAlchemy ORM
- **Additional Libraries**: 
  - Chart.js for statistics visualization
  - QRCode.js for QR code generation
  - Lucide for icons

## 💻 Key Components

### Frontend

1. **Responsive Layout**: 
   - Flexbox and Grid for layout
   - Mobile-first approach with responsive breakpoints

2. **Interactive UI Elements**:
   - Custom form inputs with animations
   - Animated buttons with hover effects
   - Toast notifications for user feedback

3. **Dark Mode Toggle**:
   - CSS variables for easy theme switching
   - Persistent theme preference using local storage

4. **Dynamic Content Loading**:
   - AJAX calls for seamless content updates
   - Loading spinner for better UX during API calls

5. **Data Visualization**:
   - Chart.js integration for displaying URL click statistics
   - Responsive charts that adapt to theme changes

### Backend

1. **RESTful API Endpoints**:
   - `/shorten`: POST request for creating short URLs
   - `/<short_code>`: GET request for redirecting to original URLs
   - `/stats`: GET request for fetching usage statistics

2. **Database Models**:
   - `Url` model for storing URL data
   - Fields: id, original_url, short_code, created_at, clicks

3. **URL Processing**:
   - Custom short code validation
   - Automatic short code generation
   - Duplicate checking for custom codes

4. **Statistics Tracking**:
   - Click counting for each shortened URL
   - Weekly stats aggregation for the dashboard

5. **Error Handling**:
   - Proper error responses for invalid requests
   - Logging for server-side errors

## 🚀 Getting Started

To run this application locally:

1. Clone the repository:
```bash
git clone https://github.com/tanbaycu/customurl.git

cd customurl
```

2. Install the required Python packages:
```bash
pip install flask flask_sqlalchemy
```
3. Run the Flask application:
```bash
python app.py
```

4. Open your browser and navigate to `http://localhost:5000`

## 🎨 Customization

Feel free to customize the application:

- Modify the CSS variables in the `:root` selector to change the color scheme
- Add new features to both the frontend and backend components
- Extend the `Url` model to include additional metadata for URLs

## 🔒 Security Considerations

- Implement rate limiting to prevent abuse of the URL shortening service
- Add user authentication for personalized URL management
- Use HTTPS in production to encrypt data in transit
- Sanitize and validate all user inputs to prevent XSS and SQL injection attacks

## 📈 Future Enhancements

- User accounts and authentication
- Advanced analytics for URL performance
- API key generation for programmatic access
- Bulk URL shortening feature
- Custom domain support for branded short links

## 🤝 Contributing

We welcome contributions to improve this URL shortener application. Here's how you can contribute:

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 👨‍💻 Contact
> You can see me here: [tanbaycu](https://linktr.ee/tanbaycu)


## 🙏 Acknowledgements

- [Tailwind CSS](https://tailwindcss.com/) for the utility-first CSS framework
- [Chart.js](https://www.chartjs.org/) for beautiful, animated charts
- [QRCode.js](https://davidshimjs.github.io/qrcodejs/) for QR code generation
- [Lucide](https://lucide.dev/) for the sleek, customizable icons

Happy coding! 🎉



---

