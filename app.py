from flask import Flask, render_template, request, jsonify, session, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import sqlite3
import requests
import os
import base64
from werkzeug.utils import secure_filename
import json
from config import config
from vertex_ai_service_safe import VertexAIService
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)

# Load configuration
config_name = os.environ.get('FLASK_CONFIG') or 'default'
app.config.from_object(config[config_name])

db = SQLAlchemy(app)

# Initialize Vertex AI Service
vertex_ai = VertexAIService()

# Ensure upload directory exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Helper function to check allowed file extensions
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

# Database Models
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(15), unique=True, nullable=False)
    location = db.Column(db.String(100), nullable=True)
    language = db.Column(db.String(10), default='en')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class ChatHistory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
    question = db.Column(db.Text, nullable=False)
    answer = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

class CropDiagnosis(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
    image_path = db.Column(db.String(200), nullable=False)
    diagnosis = db.Column(db.Text, nullable=False)
    confidence = db.Column(db.Float, default=0.0)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

class ForumPost(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)
    image_path = db.Column(db.String(200), nullable=True)
    likes = db.Column(db.Integer, default=0)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

class ForumReply(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    post_id = db.Column(db.Integer, db.ForeignKey('forum_post.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    content = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

# AI Chat responses for demo (replace with actual AI API)
DEMO_RESPONSES = {
    'weather': "Based on current conditions, expect moderate rainfall in the next 3 days. Perfect time for transplanting rice seedlings. Keep drainage channels ready.",
    'pest': "The symptoms you describe sound like aphids. Spray neem oil solution (20ml per liter water) early morning or evening. Repeat after 7 days.",
    'fertilizer': "For your wheat crop, apply NPK 12:32:16 at 125kg per hectare during sowing. Follow with urea (87kg/hectare) after first irrigation.",
    'price': "Current market prices in your area: Wheat ₹2,100/quintal, Rice ₹1,950/quintal, Sugarcane ₹350/quintal. Prices updated 2 hours ago.",
    'irrigation': "For drip irrigation setup, space emitters 30cm apart for vegetables. Water daily for 30-45 minutes in sandy soil, alternate days in clay soil."
}

# Farming tips data
FARMING_TIPS = {
    'irrigation': [
        {
            'title': 'Drip Irrigation Setup',
            'content': 'Install drip irrigation to save 40-60% water. Space emitters 30cm apart for vegetables.',
            'icon': '💧'
        },
        {
            'title': 'Water Schedule',
            'content': 'Water early morning (5-7 AM) or evening (6-8 PM) to reduce evaporation.',
            'icon': '⏰'
        }
    ],
    'sowing': [
        {
            'title': 'Seed Treatment',
            'content': 'Treat seeds with fungicide before sowing to prevent soil-borne diseases.',
            'icon': '🌱'
        },
        {
            'title': 'Spacing Guidelines',
            'content': 'Maintain proper spacing: Rice 20x15cm, Wheat 22cm rows, Maize 60x20cm.',
            'icon': '📏'
        }
    ],
    'harvesting': [
        {
            'title': 'Harvest Timing',
            'content': 'Harvest when grain moisture is 20-25% for better storage and quality.',
            'icon': '🌾'
        },
        {
            'title': 'Post Harvest',
            'content': 'Dry harvested grains to 12-14% moisture content before storage.',
            'icon': '☀️'
        }
    ]
}

# Routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        data = request.get_json() if request.is_json else request.form
        phone = data.get('phone')
        name = data.get('name')
        
        user = User.query.filter_by(phone=phone).first()
        if not user:
            user = User(phone=phone, name=name)
            db.session.add(user)
            db.session.commit()
        
        session['user_id'] = user.id
        session['user_name'] = user.name
        
        if request.is_json:
            return jsonify({'success': True, 'redirect': url_for('dashboard')})
        return redirect(url_for('dashboard'))
    
    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    # Get recent chat history
    recent_chats = ChatHistory.query.filter_by(user_id=session['user_id']).order_by(ChatHistory.timestamp.desc()).limit(3).all()
    
    return render_template('dashboard.html', 
                         user_name=session.get('user_name'),
                         datetime=datetime,
                         recent_chats=recent_chats)

@app.route('/chat')
def chat():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    chat_history = ChatHistory.query.filter_by(user_id=session['user_id']).order_by(ChatHistory.timestamp.desc()).limit(10).all()
    return render_template('chat.html', chat_history=chat_history)

@app.route('/ask', methods=['POST'])
def ask_question():
    data = request.get_json()
    question = data.get('question', '').strip()
    
    if not question:
        return jsonify({'answer': 'Please ask a question about farming.', 'timestamp': datetime.now().strftime('%H:%M')})
    
    # Use Vertex AI for intelligent responses
    try:
        # Determine if this is a scheme-related question
        scheme_keywords = ['scheme', 'subsidy', 'government', 'pm-kisan', 'insurance', 'loan', 'credit', 'yojana']
        is_scheme_query = any(keyword in question.lower() for keyword in scheme_keywords)
        
        if is_scheme_query:
            # Use scheme navigator
            result = vertex_ai.answer_scheme_query(question, language="english")
            if result.get('success'):
                answer_data = result.get('answer', {})
                response = f"""{answer_data.get('scheme_name', 'Government Scheme Information')}

{answer_data.get('description', 'Scheme information available through local agricultural office.')}

Eligibility: {answer_data.get('eligibility', 'Check with local office')}
Benefits: {answer_data.get('benefits', 'Various benefits available')}

Apply at: {answer_data.get('application_process', 'Visit local agricultural office')}"""
            else:
                response = "I can help you with government schemes like PM-KISAN, crop insurance, and subsidies. Please contact your local agricultural office for detailed information."
        else:
            # General farming question - check for market queries
            market_keywords = ['price', 'sell', 'market', 'rate', 'mandi', 'cost']
            is_market_query = any(keyword in question.lower() for keyword in market_keywords)
            
            if is_market_query:
                # Extract crop name from question
                crops = ['rice', 'wheat', 'tomato', 'onion', 'potato', 'sugarcane', 'cotton', 'maize']
                crop_found = next((crop for crop in crops if crop in question.lower()), 'general crop')
                
                result = vertex_ai.analyze_market_trends(crop_found, "Karnataka")
                if result.get('success'):
                    analysis = result.get('analysis', {})
                    prices = result.get('current_prices', {})
                    response = f"""Market Analysis for {crop_found.title()}

Current Price: {prices.get('current_price', 'Check local mandi')}
Trend: {analysis.get('trend', 'Stable').title()}

Recommendation: {analysis.get('recommendation', 'WAIT')}

{analysis.get('reasoning', 'Market conditions are moderate.')}

Best Markets: {', '.join(analysis.get('best_markets', ['Local Mandi']))}"""
                else:
                    response = "Current market prices are moderate. I recommend checking with your local mandi for the latest rates."
            else:
                # Use existing demo responses for other queries
                question_lower = question.lower()
                if any(word in question_lower for word in ['weather', 'rain', 'temperature']):
                    response = DEMO_RESPONSES['weather']
                elif any(word in question_lower for word in ['pest', 'insect', 'bug', 'disease']):
                    response = DEMO_RESPONSES['pest']
                elif any(word in question_lower for word in ['fertilizer', 'nutrients', 'npk']):
                    response = DEMO_RESPONSES['fertilizer']
                elif any(word in question_lower for word in ['water', 'irrigation', 'drip']):
                    response = DEMO_RESPONSES['irrigation']
                else:
                    response = "I understand your farming question. For specific advice about crop diseases, upload a photo using our crop diagnosis feature. For market prices, ask about specific crop rates. For government schemes, mention 'scheme' or 'subsidy' in your question."
        
        # Save to database
        if 'user_id' in session:
            chat = ChatHistory(
                user_id=session['user_id'],
                question=data.get('question'),
                answer=response[:500]  # Truncate for storage
            )
            db.session.add(chat)
            db.session.commit()
        
        return jsonify({
            'answer': response,
            'timestamp': datetime.now().strftime('%H:%M')
        })
        
    except Exception as e:
        print(f"Error in ask_question: {e}")
        return jsonify({
            'answer': 'I apologize, but I am having trouble right now. Please try again later or contact your local agricultural extension officer for immediate help.',
            'timestamp': datetime.now().strftime('%H:%M')
        })

@app.route('/weather')
def weather():
    # Mock weather data (replace with actual weather API)
    weather_data = {
        'location': 'Your Area',
        'temperature': 28,
        'humidity': 65,
        'rainfall': 'Light rain expected',
        'wind': '15 km/h',
        'forecast': [
            {'day': 'Today', 'temp': 28, 'condition': 'Partly Cloudy', 'icon': '⛅'},
            {'day': 'Tomorrow', 'temp': 30, 'condition': 'Sunny', 'icon': '☀️'},
            {'day': 'Day 3', 'temp': 26, 'condition': 'Rainy', 'icon': '🌧️'}
        ]
    }
    return render_template('weather.html', weather=weather_data)

@app.route('/market')
def market():
    # Mock market data (replace with actual market price API)
    market_data = [
        {'crop': 'Wheat', 'price': 2100, 'change': '+50', 'icon': '🌾'},
        {'crop': 'Rice', 'price': 1950, 'change': '-25', 'icon': '🍚'},
        {'crop': 'Maize', 'price': 1800, 'change': '+30', 'icon': '🌽'},
        {'crop': 'Sugarcane', 'price': 350, 'change': '+10', 'icon': '🎋'},
        {'crop': 'Cotton', 'price': 5200, 'change': '-100', 'icon': '🌱'},
        {'crop': 'Soybean', 'price': 4500, 'change': '+150', 'icon': '🫛'}
    ]
    return render_template('market.html', crops=market_data)

@app.route('/diagnosis')
def diagnosis():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    recent_diagnoses = CropDiagnosis.query.filter_by(user_id=session['user_id']).order_by(CropDiagnosis.timestamp.desc()).limit(5).all()
    return render_template('diagnosis.html', recent_diagnoses=recent_diagnoses)

@app.route('/upload_crop_image', methods=['POST'])
def upload_crop_image():
    if 'image' not in request.files:
        return jsonify({'error': 'No image uploaded'})
    
    file = request.files['image']
    if file.filename == '':
        return jsonify({'error': 'No image selected'})
    
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"{timestamp}_{filename}"
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        # Get crop type from form data
        crop_type = request.form.get('crop_type', 'unknown')
        
        # Use Vertex AI for crop disease diagnosis
        try:
            # Read the uploaded image
            with open(filepath, 'rb') as image_file:
                image_data = image_file.read()
            
            # Get AI diagnosis
            ai_result = vertex_ai.diagnose_crop_disease(image_data, crop_type)
            
            if ai_result.get('success'):
                diagnosis_data = ai_result.get('diagnosis', {})
                diagnosis_result = {
                    'disease': diagnosis_data.get('disease_name', 'Analysis complete'),
                    'confidence': diagnosis_data.get('confidence', 7) * 10,  # Convert to percentage
                    'remedy': '. '.join(diagnosis_data.get('treatments', ['Consult agricultural expert'])),
                    'severity': diagnosis_data.get('severity', 'moderate').title(),
                    'symptoms': diagnosis_data.get('symptoms', 'Please monitor plant condition'),
                    'prevention': '. '.join(diagnosis_data.get('prevention', ['Regular care needed'])),
                    'kannada_info': diagnosis_data.get('kannada_names', {})
                }
            else:
                # Fallback to mock diagnosis
                diagnosis_result = {
                    'disease': 'Plant Analysis Complete',
                    'confidence': 75.0,
                    'remedy': 'Monitor plant health regularly. Ensure proper watering and nutrition.',
                    'severity': 'Monitor',
                    'symptoms': 'Image processed successfully',
                    'prevention': 'Regular inspection and care'
                }
        except Exception as e:
            print(f"Error in AI diagnosis: {e}")
            # Fallback diagnosis
            diagnosis_result = {
                'disease': 'Image Analysis',
                'confidence': 70.0,
                'remedy': 'Image uploaded successfully. Please monitor plant health and consult local agricultural expert if needed.',
                'severity': 'Monitor'
            }
        
        # Save to database
        if 'user_id' in session:
            diagnosis = CropDiagnosis(
                user_id=session['user_id'],
                image_path=filename,
                diagnosis=f"Disease: {diagnosis_result['disease']}, Remedy: {diagnosis_result['remedy'][:200]}",
                confidence=diagnosis_result['confidence']
            )
            db.session.add(diagnosis)
            db.session.commit()
        
        return jsonify({
            'success': True,
            'diagnosis': diagnosis_result,
            'image_url': f"/static/uploads/{filename}"
        })
    else:
        return jsonify({'error': 'Invalid file type. Please upload an image file (JPG, PNG, WEBP).'})

@app.route('/tips')
def tips():
    return render_template('tips.html', tips=FARMING_TIPS)

@app.route('/forum')
def forum():
    posts = ForumPost.query.order_by(ForumPost.timestamp.desc()).limit(20).all()
    return render_template('forum.html', posts=posts)

@app.route('/create_post', methods=['POST'])
def create_post():
    if 'user_id' not in session:
        return jsonify({'error': 'Please login first'})
    
    data = request.get_json()
    post = ForumPost(
        user_id=session['user_id'],
        title=data.get('title'),
        content=data.get('content')
    )
    db.session.add(post)
    db.session.commit()
    
    return jsonify({'success': True})

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

# Initialize database
def create_tables():
    """Create database tables"""
    with app.app_context():
        db.create_all()
        print("Database tables created successfully!")

# Voice input route
@app.route('/voice_input', methods=['POST'])
def voice_input():
    try:
        if 'audio' not in request.files:
            return jsonify({'error': 'No audio file provided'})
        
        audio_file = request.files['audio']
        if audio_file.filename == '':
            return jsonify({'error': 'No audio file selected'})
        
        # Save the audio file temporarily
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        audio_filename = f"voice_{timestamp}.wav"
        audio_filepath = os.path.join(app.config['UPLOAD_FOLDER'], audio_filename)
        audio_file.save(audio_filepath)
        
        # Convert speech to text
        with open(audio_filepath, 'rb') as audio_data:
            audio_content = audio_data.read()
        
        text_result = vertex_ai.speech_to_text(audio_content)
        
        if text_result.get('success'):
            transcribed_text = text_result.get('text', '')
            
            # Get AI response for the transcribed text
            ai_response = vertex_ai.ask_question(transcribed_text)
            response_text = ai_response.get('answer', 'I did not understand your question.')
            
            # Convert response to speech
            speech_result = vertex_ai.text_to_speech(response_text)
            
            if speech_result.get('success'):
                audio_base64 = speech_result.get('audio_base64', '')
                return jsonify({
                    'success': True,
                    'transcribed_text': transcribed_text,
                    'response_text': response_text,
                    'audio_response': audio_base64
                })
            else:
                return jsonify({
                    'success': True,
                    'transcribed_text': transcribed_text,
                    'response_text': response_text,
                    'audio_response': None
                })
        else:
            return jsonify({'error': 'Failed to process voice input'})
            
    except Exception as e:
        print(f"Voice input error: {e}")
        return jsonify({'error': 'Voice processing failed'})
    finally:
        # Clean up temporary audio file
        if 'audio_filepath' in locals() and os.path.exists(audio_filepath):
            os.remove(audio_filepath)

# Text to speech route
@app.route('/text_to_speech', methods=['POST'])
def text_to_speech():
    try:
        data = request.get_json()
        text = data.get('text', '')
        
        if not text:
            return jsonify({'error': 'No text provided'})
        
        speech_result = vertex_ai.text_to_speech(text)
        
        if speech_result.get('success'):
            return jsonify({
                'success': True,
                'audio_base64': speech_result.get('audio_base64', '')
            })
        else:
            return jsonify({'error': 'Failed to convert text to speech'})
            
    except Exception as e:
        print(f"Text to speech error: {e}")
        return jsonify({'error': 'Text to speech conversion failed'})

# Get voice-enabled chat response
@app.route('/voice_chat', methods=['POST'])
def voice_chat():
    try:
        data = request.get_json()
        message = data.get('message', '')
        include_audio = data.get('include_audio', False)
        
        if not message:
            return jsonify({'error': 'No message provided'})
        
        # Get AI response
        ai_response = vertex_ai.ask_question(message)
        response_text = ai_response.get('answer', 'I did not understand your question.')
        
        result = {
            'success': True,
            'response': response_text
        }
        
        # Add audio if requested
        if include_audio:
            speech_result = vertex_ai.text_to_speech(response_text)
            if speech_result.get('success'):
                result['audio_base64'] = speech_result.get('audio_base64', '')
        
        return jsonify(result)
        
    except Exception as e:
        print(f"Voice chat error: {e}")
        return jsonify({'error': 'Voice chat failed'})

# Error handlers
@app.errorhandler(404)
def not_found_error(error):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template('404.html'), 500

# Favicon route
@app.route('/favicon.ico')
def favicon():
    return '', 204  # Return empty response with no content

if __name__ == '__main__':
    create_tables()
    port = int(os.environ.get('PORT', 5000))
    debug = app.config.get('DEBUG', False)
    app.run(debug=debug, host='0.0.0.0', port=port)
