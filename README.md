# Project Kisan - AI-Powered Farming Assistant �

An AI-powered web application designed to help rural farmers with crop disease diagnosis, market analysis, government scheme navigation, and agricultural guidance through voice-first, multilingual interactions.

## Features

### 🤖 AI Chat Assistant
- Natural language questions about farming
- Intelligent responses for farming questions
- Government scheme information and guidance
- Market price analysis and trends
- Weather and irrigation advice

### � Voice-First Interface
- Speech-to-text input (Kannada and English)
- Text-to-speech output for responses
- Voice mode toggle for hands-free operation
- Multilingual support for local farmers

### � Crop Disease Diagnosis
- Upload crop images for AI analysis
- Gemini Vision-powered disease detection
- Detailed treatment recommendations
- Severity assessment and prevention tips
- Kannada language support for local names

### 🌾 Smart Farming Features
- Market trend analysis for major crops
- Weather and irrigation guidance
- Organic farming recommendations
- Government scheme navigator
- Pest management strategies

### 👥 Community Forum
- Connect with other farmers
- Share experiences and tips
- Ask questions and get expert advice
- Moderated content to prevent misinformation

## Technology Stack

- **Backend**: Flask with SQLAlchemy
- **AI Services**: Google Vertex AI with Gemini models
- **Voice Processing**: Google Cloud Speech-to-Text and Text-to-Speech
- **Language**: Kannada (kn-IN) and English support
- **Frontend**: Responsive design with Tailwind CSS
- **Database**: SQLite (development), PostgreSQL (production)

## Quick Start

### Prerequisites
- Python 3.8 or higher
- pip package manager

### Installation

1. **Clone or navigate to the project directory**
   ```bash
   cd kisan
   ```

2. **Create a virtual environment** (recommended)
   ```bash
   python -m venv venv
   venv\Scripts\activate  # On Windows
   # source venv/bin/activate  # On macOS/Linux
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the application**
   ```bash
   python app.py
   ```

5. **Open your browser**
   Navigate to `http://localhost:5000`

## Usage

### First Time Setup
1. Open the application in your browser
2. Click "Get Started" or "Login"
3. Enter your name and phone number
4. Select your preferred language
5. Start using the features!

### Using the AI Chat
1. Go to the Dashboard and click "AI Chat"
2. Type your farming question or use the microphone for voice input
3. Get instant responses with voice output option
4. Use quick suggestion buttons for common questions

### Crop Diagnosis
1. Navigate to "Crop Diagnosis"
2. Upload a photo of your plant or take one with your camera
3. Wait for AI analysis (usually takes 10-15 seconds)
4. Get detailed diagnosis with treatment recommendations
5. Download or save the report for future reference

### Weather & Market Info
- Check current weather and 7-day forecast
- View real-time crop prices from nearby markets
- Set price alerts for your crops
- Get farming recommendations based on weather

## Configuration

### Environment Variables
Create a `.env` file in the project root for production:

```env
SECRET_KEY=your-secret-key-here
OPENAI_API_KEY=your-openai-api-key
WEATHER_API_KEY=your-weather-api-key
DATABASE_URL=your-database-url
```

### Features Configuration
Edit `config.py` to enable/disable features:
- Voice features
- Offline mode
- Notifications
- Supported languages

## Project Structure

```
kisan/
├── app.py              # Main Flask application
├── config.py           # Configuration settings
├── requirements.txt    # Python dependencies
├── templates/          # HTML templates
│   ├── base.html
│   ├── index.html
│   ├── login.html
│   ├── dashboard.html
│   ├── chat.html
│   ├── weather.html
│   ├── market.html
│   ├── diagnosis.html
│   ├── tips.html
│   └── forum.html
├── static/            # Static files
│   ├── style.css
│   ├── app.js
│   └── uploads/       # Uploaded images
└── README.md
```

## Key Features Explained

### 🎯 Farmer-Friendly Design
- Large buttons and fonts for mobile use
- Icons and visuals for low-literacy users
- Color-coded sections (green for healthy, red for alerts)
- Minimal text complexity

### 🌐 Offline-Ready
- Works with poor internet connectivity
- Saves chat history and diagnoses locally
- Cached weather and market data
- Service worker for offline functionality

### 🔊 Voice Support
- Speech-to-text for input (works on modern browsers)
- Text-to-speech for output
- Hands-free operation for illiterate farmers
- Multiple language support

### 📱 Mobile-First
- Responsive design for smartphones
- Touch-friendly interface
- Optimized for slow internet connections
- Progressive Web App (PWA) capabilities

## Deployment

### Local Development
The application runs on `http://localhost:5000` by default.

### Production Deployment
Suitable for deployment on:
- Railway
- Render
- PythonAnywhere
- Heroku
- Any VPS with Python support

### Database Migration
For production, consider migrating from SQLite to PostgreSQL:
1. Install psycopg2-binary
2. Update DATABASE_URL in environment
3. The app will automatically create tables

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## API Integration

### Weather API
Currently uses mock data. To integrate real weather:
1. Get API key from OpenWeatherMap or similar
2. Update weather route in app.py
3. Add API key to environment variables

### Market Prices API
Mock data provided. For real market data:
1. Integrate with government agriculture APIs
2. Add data sources in config.py
3. Update market route with real API calls

### AI Model
Currently uses rule-based responses. For real AI:
1. Add OpenAI API key to environment
2. Update ask_question route
3. Configure AI prompts for farming context

## Troubleshooting

### Common Issues

**Voice recognition not working**
- Ensure you're using HTTPS or localhost
- Check browser compatibility (Chrome/Safari work best)
- Grant microphone permissions

**Image upload failing**
- Check file size (max 16MB)
- Ensure supported format (JPG, PNG, WebP)
- Verify upload directory permissions

**Database errors**
- Delete kisan.db and restart app
- Check file permissions in project directory

## License

This project is open source and available under the MIT License.

## Support

For support or questions:
- Create an issue on GitHub
- Check the troubleshooting section
- Review the configuration options

---

**Built with ❤️ for farmers** 🌾

*Kisan+ aims to bridge the digital divide in agriculture by providing AI-powered assistance that's accessible, affordable, and farmer-friendly.*
