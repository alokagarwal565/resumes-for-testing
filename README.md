# Resume Generator - Deployed on Vercel

A modern web application that generates customizable numbers of random sample resumes in PDF format. Successfully deployed on Vercel with a beautiful, responsive interface.

## 🌐 Live Application

**Production URL**: https://resumes-for-testing.vercel.app/

## ✨ Features

- **Web Interface**: Beautiful, responsive design with modern UI
- **Customizable Generation**: Choose how many resumes to generate (1-50)
- **Two Content Types**: 
  - Template-based (fast generation)
  - Gemini AI-enhanced (premium content)
- **Real-time Progress**: Live progress tracking during generation
- **ZIP Download**: All resumes packaged in a downloadable ZIP file
- **Mobile Responsive**: Works perfectly on all devices

## 🚀 Quick Start

1. **Visit the app**: Go to the production URL above
2. **Enter number of resumes**: Choose between 1-50 resumes
3. **Select content type**: Template-based or Gemini AI
4. **Generate**: Click the generate button and wait
5. **Download**: Get your ZIP file with all resumes

## 📁 Project Structure

```
resume-generator/
├── app.py                 # Flask application (Vercel-compatible)
├── resume_generator.py    # Core resume generation logic
├── vercel.json           # Vercel deployment configuration
├── requirements.txt      # Python dependencies
├── templates/
│   └── index.html        # Main web page
├── static/
│   ├── styles.css        # CSS styling
│   └── script.js         # JavaScript functionality
└── README.md             # This file
```

## 🛠️ Technical Details

### Backend
- **Flask**: Python web framework
- **ReportLab**: PDF generation
- **Google Generative AI**: Optional enhanced content generation
- **Vercel**: Serverless deployment platform

### Frontend
- **HTML5**: Semantic markup
- **CSS3**: Modern styling with animations
- **JavaScript**: Interactive functionality
- **Font Awesome**: Icons

### Deployment
- **Platform**: Vercel
- **Runtime**: Python 3.9+
- **Architecture**: Serverless functions
- **CDN**: Global content delivery

## ⚠️ Vercel Limitations

- **Resume Limit**: Maximum 50 resumes per request
- **Processing Time**: 10 seconds (Hobby) or 5 minutes (Pro)
- **Memory**: In-memory processing only
- **Cold Starts**: Initial requests may be slower

## 🔧 Local Development

If you want to run this locally:

```bash
# Install dependencies
pip install -r requirements.txt

# Run the application
python app.py

# Visit http://localhost:5000
```

## 📊 Sample Resume Data

Each generated resume includes:
- **Personal Information**: Name, email, phone, address
- **Professional Summary**: Career overview
- **Education**: Degree, major, university, GPA, graduation year
- **Work Experience**: 1-4 previous positions with detailed descriptions
- **Technical Skills**: 8-15 relevant technical skills

## 🎯 Use Cases

- **Testing ATS Systems**: Generate sample resumes for testing
- **Demo Purposes**: Show resume formats and layouts
- **Training Data**: Create datasets for machine learning
- **Prototyping**: Test resume parsing applications
- **Education**: Learn about resume structure and content

## 🔒 Privacy & Security

- **No Data Storage**: All processing happens in memory
- **No Persistence**: Files are generated and downloaded immediately
- **API Keys**: Store Gemini API keys securely in environment variables
- **Input Validation**: Server-side validation prevents malicious input

## 📈 Performance

- **Generation Speed**: ~0.1-0.5 seconds per resume
- **Memory Usage**: ~1-2MB per resume
- **Concurrent Users**: Supports multiple simultaneous requests
- **Global CDN**: Fast loading worldwide

## 🆘 Support

- **Issues**: Check the browser console for errors
- **Limits**: Reduce resume count if experiencing timeouts
- **API Keys**: Ensure Gemini API key is valid if using AI mode
- **Browser**: Use modern browsers for best experience

## 📝 License

This project is open source and available under the MIT License.

## 🎉 Success!

Your Resume Generator is now live and accessible worldwide! 

**Visit**: https://resumes-for-testing.vercel.app/

---

*Built with ❤️ using Python, Flask, and modern web technologies*