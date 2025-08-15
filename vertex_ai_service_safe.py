"""
Safe Vertex AI Service for Project Kisan
Handles all AI interactions with proper fallback for development
"""

import os
import base64
import json
import logging
from typing import Dict, Any, Optional
from datetime import datetime

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class VertexAIService:
    def __init__(self):
        """Initialize the Vertex AI service with safe configuration."""
        self.project_id = os.getenv('GOOGLE_CLOUD_PROJECT_ID', 'kisan-farming-ai')
        self.location = os.getenv('GOOGLE_CLOUD_LOCATION', 'us-central1')
        self.development_mode = True  # Always start in development mode
        
        logger.info("Vertex AI Service initialized in safe development mode")
    
    def diagnose_crop_disease(self, image_data: bytes, crop_type: str = "unknown") -> Dict[str, Any]:
        """
        Analyze crop image for disease detection using Gemini Vision.
        Falls back to mock response in development mode.
        """
        try:
            if self.development_mode:
                return self._get_mock_diagnosis(crop_type)
            
            # Real AI implementation would go here
            return self._get_mock_diagnosis(crop_type)
            
        except Exception as e:
            logger.error(f"Error in crop diagnosis: {e}")
            return {
                'success': False,
                'error': str(e),
                'diagnosis': self._get_mock_diagnosis(crop_type).get('diagnosis', {})
            }
    
    def _get_mock_diagnosis(self, crop_type: str) -> Dict[str, Any]:
        """Generate mock diagnosis response."""
        diagnoses = {
            'tomato': {
                'disease_name': 'Early Blight',
                'confidence': 8.5,
                'severity': 'moderate',
                'symptoms': 'Dark spots on leaves with yellow halos',
                'treatments': [
                    'Apply copper-based fungicide',
                    'Remove affected leaves',
                    'Improve air circulation',
                    'Reduce watering frequency'
                ],
                'prevention': [
                    'Crop rotation',
                    'Proper spacing between plants',
                    'Avoid overhead watering',
                    'Use disease-resistant varieties'
                ],
                'kannada_names': {
                    'disease': 'ಆರಂಭಿಕ ಕಲೆ',
                    'crop': 'ಟೊಮೇಟೊ'
                }
            },
            'rice': {
                'disease_name': 'Blast Disease',
                'confidence': 9.2,
                'severity': 'high',
                'symptoms': 'Diamond-shaped lesions on leaves',
                'treatments': [
                    'Apply tricyclazole fungicide',
                    'Maintain proper water management',
                    'Apply balanced fertilizer',
                    'Remove infected plant debris'
                ],
                'prevention': [
                    'Use resistant varieties',
                    'Proper seed treatment',
                    'Balanced nutrition',
                    'Avoid excessive nitrogen'
                ],
                'kannada_names': {
                    'disease': 'ಬ್ಲಾಸ್ಟ್ ರೋಗ',
                    'crop': 'ಅಕ್ಕಿ'
                }
            },
            'wheat': {
                'disease_name': 'Rust Disease',
                'confidence': 8.8,
                'severity': 'moderate',
                'symptoms': 'Orange-red pustules on leaves',
                'treatments': [
                    'Apply triazole fungicides',
                    'Early detection and treatment',
                    'Remove volunteer wheat plants',
                    'Monitor weather conditions'
                ],
                'prevention': [
                    'Plant resistant varieties',
                    'Proper crop rotation',
                    'Timely sowing',
                    'Field sanitation'
                ],
                'kannada_names': {
                    'disease': 'ತುಕ್ಕು ರೋಗ',
                    'crop': 'ಗೋಧಿ'
                }
            }
        }
        
        # Get diagnosis based on crop type or default
        diagnosis = diagnoses.get(crop_type.lower(), diagnoses['tomato'])
        
        return {
            'success': True,
            'diagnosis': diagnosis
        }
    
    def ask_question(self, question: str) -> Dict[str, Any]:
        """
        Process general farming questions using Gemini Pro.
        Falls back to mock responses in development mode.
        """
        try:
            if self.development_mode:
                return self._get_mock_answer(question)
            
            # Real AI implementation would go here
            return self._get_mock_answer(question)
            
        except Exception as e:
            logger.error(f"Error in question processing: {e}")
            return {
                'success': False,
                'answer': 'Sorry, I encountered an error processing your question.',
                'error': str(e)
            }
    
    def _get_mock_answer(self, question: str) -> Dict[str, Any]:
        """Generate intelligent mock responses based on question content."""
        question_lower = question.lower()
        
        # Scheme-related questions
        if any(word in question_lower for word in ['scheme', 'subsidy', 'government', 'loan', 'credit']):
            return {
                'success': True,
                'answer': """**Government Schemes for Farmers:**

🏛️ **PM-KISAN Scheme**: ₹6,000 per year direct benefit transfer
📋 **Eligibility**: All farmer families owning cultivable land
📞 **Apply**: Visit pmkisan.gov.in or nearest CSC

🌾 **Crop Insurance**: Pradhan Mantri Fasal Bima Yojana
💰 **Premium**: 2% for Kharif, 1.5% for Rabi crops
🛡️ **Coverage**: Natural calamities, pests, diseases

💳 **KCC (Kisan Credit Card)**: Easy agricultural loans
🏦 **Interest**: 7% (with 3% subvention = 4% effective)
⏰ **Repayment**: Flexible based on crop cycle

For more details, visit your nearest agriculture office or call 1800-180-1551"""
            }
        
        # Market price questions
        elif any(word in question_lower for word in ['price', 'market', 'rate', 'sell', 'mandi']):
            return {
                'success': True,
                'answer': """**Current Market Prices (Indicative):**

🌾 **Wheat**: ₹2,125/quintal (MSP: ₹2,125)
🍚 **Rice**: ₹2,060/quintal (MSP: ₹2,060)
🌽 **Maize**: ₹1,870/quintal (MSP: ₹1,870)
🫘 **Arhar Dal**: ₹6,600/quintal (MSP: ₹6,600)

📍 **Best Markets**: Check eNAM portal (enam.gov.in)
📱 **Mobile App**: Download 'eNAM' app for live prices
💡 **Tip**: Compare prices across multiple mandis before selling

*Prices vary by location and quality. Always verify current rates."""
            }
        
        # Weather and irrigation
        elif any(word in question_lower for word in ['weather', 'rain', 'irrigation', 'water', 'drought']):
            return {
                'success': True,
                'answer': """**Weather & Irrigation Guidelines:**

🌦️ **Current Season**: Monitor IMD weather forecasts
📱 **Apps**: Meghdoot, Pusa Krishi, Kisan Suvidha

💧 **Irrigation Tips**:
• Early morning (5-8 AM) or evening (5-7 PM)
• Drip irrigation saves 30-40% water
• Mulching reduces water requirement

🌾 **Crop-specific watering**:
• Rice: Maintain 2-5 cm standing water
• Wheat: 4-5 irrigations in entire season
• Cotton: Deep watering every 10-15 days

⚠️ **Weather alerts**: Sign up for SMS alerts on weather.gov.in"""
            }
        
        # Fertilizer and nutrition
        elif any(word in question_lower for word in ['fertilizer', 'nutrition', 'nutrients', 'manure', 'compost']):
            return {
                'success': True,
                'answer': """**Fertilizer & Nutrition Guide:**

🧪 **Soil Testing**: Get soil tested every 2-3 years
📍 **Where**: Nearest Soil Health Card center

⚖️ **NPK Ratio Guidelines**:
• Cereals: 4:2:1 (N:P:K)
• Pulses: 1:2:1 (with Rhizobium culture)
• Vegetables: 4:2:4

🌱 **Organic Options**:
• Vermicompost: 2-3 tons/hectare
• FYM: 5-10 tons/hectare
• Biofertilizers: Azotobacter, PSB

💰 **Subsidy**: 50% subsidy on fertilizers through PM-JAN program
📱 **Booking**: Use iFMS app for fertilizer availability"""
            }
        
        # Pest and disease management
        elif any(word in question_lower for word in ['pest', 'disease', 'insect', 'fungus', 'treatment']):
            return {
                'success': True,
                'answer': """**Pest & Disease Management:**

🔍 **Early Detection**:
• Regular field monitoring (every 2-3 days)
• Use pheromone traps
• Yellow sticky traps for flying insects

🌿 **Organic Solutions**:
• Neem oil spray (5ml/liter water)
• Bt spray for caterpillars
• Trichoderma for soil-borne diseases

🧪 **Chemical Control** (if needed):
• Always follow label instructions
• Use recommended dosage
• Rotate different chemicals

📞 **Expert Help**: Call agriculture helpline 1800-180-1551
📱 **Apps**: Plantix app for disease identification"""
            }
        
        # General farming questions
        else:
            return {
                'success': True,
                'answer': """**General Farming Guidance:**

🌱 **Best Practices**:
• Follow crop calendar for your region
• Practice crop rotation to maintain soil health
• Use integrated pest management (IPM)
• Maintain proper field records

📚 **Knowledge Sources**:
• Agricultural universities extension services
• KVK (Krishi Vigyan Kendra) programs
• ICAR research publications
• Progressive farmer groups

📱 **Useful Apps**:
• Kisan Suvidha (weather + market)
• Plantix (crop protection)
• AgriApp (farming calendar)
• mKisan (SMS alerts)

💡 **Pro Tip**: Connect with successful farmers in your area for practical insights!"""
            }
    
    def analyze_market_trends(self, crop: str, location: str = "") -> Dict[str, Any]:
        """
        Analyze market trends for specific crops.
        Returns mock data in development mode.
        """
        try:
            if self.development_mode:
                return self._get_mock_market_analysis(crop, location)
            
            # Real AI implementation would go here
            return self._get_mock_market_analysis(crop, location)
            
        except Exception as e:
            logger.error(f"Error in market analysis: {e}")
            return {
                'success': False,
                'error': str(e)
            }
    
    def _get_mock_market_analysis(self, crop: str, location: str) -> Dict[str, Any]:
        """Generate mock market analysis."""
        market_data = {
            'rice': {
                'current_price': 2060,
                'msp': 2060,
                'trend': 'stable',
                'forecast': 'Prices expected to remain stable due to good harvest',
                'best_markets': ['Delhi', 'Mumbai', 'Kolkata'],
                'demand': 'high'
            },
            'wheat': {
                'current_price': 2125,
                'msp': 2125,
                'trend': 'increasing',
                'forecast': 'Slight increase expected due to export demand',
                'best_markets': ['Delhi', 'Kanpur', 'Ahmedabad'],
                'demand': 'high'
            },
            'tomato': {
                'current_price': 3500,
                'msp': 0,
                'trend': 'volatile',
                'forecast': 'High seasonal variation, good prices in winter',
                'best_markets': ['Bengaluru', 'Delhi', 'Mumbai'],
                'demand': 'medium'
            }
        }
        
        data = market_data.get(crop.lower(), market_data['rice'])
        
        return {
            'success': True,
            'analysis': {
                'crop': crop,
                'location': location or 'India',
                'current_price': data['current_price'],
                'msp': data['msp'],
                'trend': data['trend'],
                'forecast': data['forecast'],
                'best_markets': data['best_markets'],
                'demand_level': data['demand'],
                'recommendation': f"Based on current trends, {crop} shows {data['trend']} price movement. {data['forecast']}"
            }
        }
    
    def speech_to_text(self, audio_data: bytes) -> Dict[str, Any]:
        """
        Convert speech to text using Google Cloud Speech-to-Text.
        Returns mock response in development mode.
        """
        try:
            if self.development_mode:
                return {
                    'success': True,
                    'text': 'ನನ್ನ ಬೆಳೆಯಲ್ಲಿ ರೋಗ ಇದೆ ಎಂದು ಭಾವಿಸುತ್ತೇನೆ' # Kannada: "I think there's a disease in my crop"
                }
            
            # Real speech-to-text implementation would go here
            return {
                'success': False,
                'error': 'Speech-to-text service not available'
            }
            
        except Exception as e:
            logger.error(f"Error in speech-to-text: {e}")
            return {
                'success': False,
                'error': str(e)
            }
    
    def text_to_speech(self, text: str, language: str = 'kn-IN') -> Dict[str, Any]:
        """
        Convert text to speech using Google Cloud Text-to-Speech.
        Returns mock response in development mode.
        """
        try:
            if self.development_mode:
                # Return a simple success response (audio would be generated by browser)
                return {
                    'success': True,
                    'audio_base64': None,  # Browser will handle TTS
                    'message': 'Text-to-speech will use browser capabilities'
                }
            
            # Real text-to-speech implementation would go here
            return {
                'success': False,
                'error': 'Text-to-speech service not available'
            }
            
        except Exception as e:
            logger.error(f"Error in text-to-speech: {e}")
            return {
                'success': False,
                'error': str(e)
            }
    
    def answer_scheme_query(self, query: str) -> Dict[str, Any]:
        """
        Answer government scheme related queries.
        Uses RAG approach with government scheme database.
        """
        try:
            # For now, redirect to general question handler
            return self.ask_question(query)
            
        except Exception as e:
            logger.error(f"Error in scheme query: {e}")
            return {
                'success': False,
                'error': str(e),
                'answer': 'Sorry, I encountered an error processing your scheme query.'
            }
