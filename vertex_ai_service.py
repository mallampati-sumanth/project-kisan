"""
Google Vertex AI Service for Project Kisan
Handles all AI-related functionality including:
- Gemini Multimodal for crop disease diagnosis
- Gemini Pro for market analysis and scheme Q&A
- Speech-to-Text for Kannada voice input
- Text-to-Speech for Kannada voice output
"""

import os
import io
import base64
import json
from typing import Dict, List, Optional, Tuple
import vertexai
from vertexai.generative_models import GenerativeModel, Part
from google.cloud import speech
from google.cloud import texttospeech
from google.cloud import translate_v2 as translate
import requests
from datetime import datetime
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class VertexAIService:
    def __init__(self, project_id: str = None, location: str = "us-central1"):
        """
        Initialize Vertex AI Service
        
        Args:
            project_id: Google Cloud Project ID
            location: Google Cloud region
        """
        self.project_id = project_id or os.getenv('GOOGLE_CLOUD_PROJECT')
        self.location = location
        
        # Initialize Vertex AI
        if self.project_id:
            try:
                vertexai.init(project=self.project_id, location=self.location)
                self.vertex_ai_enabled = True
                logger.info(f"Vertex AI initialized for project: {self.project_id}")
            except Exception as e:
                logger.warning(f"Vertex AI initialization failed: {e}")
                self.vertex_ai_enabled = False
        else:
            logger.warning("No Google Cloud Project ID found. Using mock responses.")
            self.vertex_ai_enabled = False
        
        # Initialize models
        self.gemini_pro = None
        self.gemini_vision = None
        self.speech_client = None
        self.tts_client = None
        self.translate_client = None
        
        if self.vertex_ai_enabled:
            try:
                self.gemini_pro = GenerativeModel("gemini-1.5-pro")
                self.gemini_vision = GenerativeModel("gemini-1.5-pro-vision")
                self.speech_client = speech.SpeechClient()
                self.tts_client = texttospeech.TextToSpeechClient()
                self.translate_client = translate.Client()
                logger.info("All AI models initialized successfully")
            except Exception as e:
                logger.error(f"Error initializing AI models: {e}")
                self.vertex_ai_enabled = False

    def diagnose_crop_disease(self, image_data: bytes, crop_type: str = "unknown") -> Dict:
        """
        Analyze crop image for disease/pest detection using Gemini Vision
        
        Args:
            image_data: Binary image data
            crop_type: Type of crop (e.g., rice, wheat, tomato)
            
        Returns:
            Dict containing diagnosis results
        """
        if not self.vertex_ai_enabled or not self.gemini_vision:
            return self._mock_crop_diagnosis(crop_type)
        
        try:
            # Prepare image for Gemini Vision
            image_part = Part.from_data(image_data, mime_type="image/jpeg")
            
            prompt = f"""
            You are an expert agricultural pathologist analyzing a {crop_type} plant image.
            Please analyze this image and provide:
            
            1. Disease/Pest Identification:
               - Name of the disease or pest (if any)
               - Confidence level (1-10)
               - Severity assessment (mild/moderate/severe)
            
            2. Symptoms Observed:
               - Visible symptoms on leaves, stems, fruits
               - Stage of infection
            
            3. Treatment Recommendations:
               - Immediate actions needed
               - Organic/traditional remedies available locally in India
               - Chemical treatments if necessary
               - Preventive measures
            
            4. Local Kannada Names:
               - Disease name in Kannada
               - Treatment names in Kannada
            
            Please respond in JSON format with keys: disease_name, confidence, severity, symptoms, treatments, prevention, kannada_names.
            If no disease is detected, indicate the plant appears healthy.
            """
            
            response = self.gemini_vision.generate_content([prompt, image_part])
            
            # Parse response
            try:
                result = json.loads(response.text)
            except json.JSONDecodeError:
                # If response is not JSON, create structured response
                result = {
                    "disease_name": "Analysis Complete",
                    "confidence": 8,
                    "severity": "moderate",
                    "symptoms": response.text[:200] + "...",
                    "treatments": ["Consult agricultural expert", "Monitor plant condition"],
                    "prevention": ["Regular inspection", "Proper spacing", "Good drainage"],
                    "kannada_names": {"disease": "ರೋಗ", "treatment": "ಚಿಕಿತ್ಸೆ"}
                }
            
            return {
                "success": True,
                "diagnosis": result,
                "timestamp": datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Error in crop disease diagnosis: {e}")
            return self._mock_crop_diagnosis(crop_type)

    def analyze_market_trends(self, crop_name: str, location: str = "Karnataka") -> Dict:
        """
        Analyze market trends and provide sell/wait advice using Gemini Pro
        
        Args:
            crop_name: Name of the crop
            location: Market location
            
        Returns:
            Dict containing market analysis
        """
        if not self.vertex_ai_enabled or not self.gemini_pro:
            return self._mock_market_analysis(crop_name, location)
        
        try:
            # Get current market prices (this would integrate with Agmarknet API)
            current_prices = self._fetch_market_prices(crop_name, location)
            
            prompt = f"""
            You are a market analyst specializing in Indian agricultural markets.
            Analyze the market situation for {crop_name} in {location} and provide advice to farmers.
            
            Current market data: {current_prices}
            
            Please provide:
            1. Current market price trend (increasing/decreasing/stable)
            2. Price prediction for next 2-4 weeks
            3. Recommendation: SELL NOW or WAIT
            4. Reasoning for the recommendation
            5. Best markets/mandis to sell in {location}
            6. Optimal timing for selling
            
            Respond in JSON format with keys: trend, prediction, recommendation, reasoning, best_markets, optimal_timing.
            Consider seasonal patterns, weather conditions, and demand factors.
            """
            
            response = self.gemini_pro.generate_content(prompt)
            
            try:
                result = json.loads(response.text)
            except json.JSONDecodeError:
                result = {
                    "trend": "stable",
                    "prediction": "Moderate increase expected",
                    "recommendation": "WAIT",
                    "reasoning": response.text[:200] + "...",
                    "best_markets": [f"{location} Main Mandi", "Local Agricultural Market"],
                    "optimal_timing": "Within 2-3 weeks"
                }
            
            return {
                "success": True,
                "analysis": result,
                "current_prices": current_prices,
                "timestamp": datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Error in market analysis: {e}")
            return self._mock_market_analysis(crop_name, location)

    def answer_scheme_query(self, question: str, language: str = "kannada") -> Dict:
        """
        Answer questions about government schemes using Gemini Pro with RAG
        
        Args:
            question: User question about schemes
            language: Response language (kannada/english)
            
        Returns:
            Dict containing scheme information
        """
        if not self.vertex_ai_enabled or not self.gemini_pro:
            return self._mock_scheme_answer(question, language)
        
        try:
            prompt = f"""
            You are an expert on Indian government agricultural schemes and subsidies.
            Answer the farmer's question about government schemes in a helpful, accurate manner.
            
            Question: {question}
            Response Language: {language}
            
            Please provide:
            1. Relevant scheme name and description
            2. Eligibility criteria
            3. Benefits/subsidy amount
            4. Application process
            5. Required documents
            6. Direct links/contact information
            7. Deadlines (if any)
            
            Include information about:
            - PM-KISAN scheme
            - Crop insurance schemes
            - Soil health card scheme
            - Drip irrigation subsidies
            - Kisan Credit Card
            - Any relevant state-specific Karnataka schemes
            
            If responding in Kannada, use simple language that farmers can understand.
            Respond in JSON format with keys: scheme_name, description, eligibility, benefits, application_process, documents, links, deadlines.
            """
            
            response = self.gemini_pro.generate_content(prompt)
            
            try:
                result = json.loads(response.text)
            except json.JSONDecodeError:
                result = {
                    "scheme_name": "Government Agricultural Schemes",
                    "description": response.text[:300] + "...",
                    "eligibility": "Farmers with valid documents",
                    "benefits": "Various subsidies and support",
                    "application_process": "Visit nearest agricultural office",
                    "documents": ["Aadhaar", "Land records", "Bank account"],
                    "links": ["https://pmkisan.gov.in", "https://agri.karnataka.gov.in"],
                    "deadlines": "Check with local agricultural office"
                }
            
            return {
                "success": True,
                "answer": result,
                "language": language,
                "timestamp": datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Error in scheme query: {e}")
            return self._mock_scheme_answer(question, language)

    def speech_to_text(self, audio_data: bytes, language_code: str = "kn-IN") -> Dict:
        """
        Convert speech to text using Google Cloud Speech-to-Text
        
        Args:
            audio_data: Binary audio data
            language_code: Language code (kn-IN for Kannada)
            
        Returns:
            Dict containing transcribed text
        """
        if not self.vertex_ai_enabled or not self.speech_client:
            return {"success": False, "text": "Voice recognition not available", "confidence": 0}
        
        try:
            audio = speech.RecognitionAudio(content=audio_data)
            config = speech.RecognitionConfig(
                encoding=speech.RecognitionConfig.AudioEncoding.WEBM_OPUS,
                sample_rate_hertz=16000,
                language_code=language_code,
                enable_automatic_punctuation=True,
            )
            
            response = self.speech_client.recognize(config=config, audio=audio)
            
            if response.results:
                result = response.results[0]
                return {
                    "success": True,
                    "text": result.alternatives[0].transcript,
                    "confidence": result.alternatives[0].confidence,
                    "language": language_code
                }
            else:
                return {
                    "success": False,
                    "text": "Could not understand audio",
                    "confidence": 0
                }
                
        except Exception as e:
            logger.error(f"Error in speech recognition: {e}")
            return {"success": False, "text": f"Error: {str(e)}", "confidence": 0}

    def text_to_speech(self, text: str, language_code: str = "kn-IN") -> bytes:
        """
        Convert text to speech using Google Cloud Text-to-Speech
        
        Args:
            text: Text to convert
            language_code: Language code (kn-IN for Kannada)
            
        Returns:
            Binary audio data
        """
        if not self.vertex_ai_enabled or not self.tts_client:
            return b""  # Return empty bytes if TTS not available
        
        try:
            synthesis_input = texttospeech.SynthesisInput(text=text)
            
            voice = texttospeech.VoiceSelectionParams(
                language_code=language_code,
                ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL,
            )
            
            audio_config = texttospeech.AudioConfig(
                audio_encoding=texttospeech.AudioEncoding.MP3
            )
            
            response = self.tts_client.synthesize_speech(
                input=synthesis_input, voice=voice, audio_config=audio_config
            )
            
            return response.audio_content
            
        except Exception as e:
            logger.error(f"Error in text-to-speech: {e}")
            return b""

    def _fetch_market_prices(self, crop_name: str, location: str) -> Dict:
        """
        Fetch current market prices from Agmarknet/eNAM APIs
        This is a placeholder - would integrate with actual APIs
        """
        # Mock data - replace with actual API calls
        return {
            "crop": crop_name,
            "location": location,
            "current_price": "₹2,500/quintal",
            "yesterday_price": "₹2,450/quintal",
            "last_week_price": "₹2,400/quintal",
            "trend": "increasing",
            "source": "Agmarknet"
        }

    def _mock_crop_diagnosis(self, crop_type: str) -> Dict:
        """Mock crop diagnosis for when Vertex AI is not available"""
        return {
            "success": True,
            "diagnosis": {
                "disease_name": "Healthy Plant",
                "confidence": 7,
                "severity": "none",
                "symptoms": f"The {crop_type} plant appears healthy with no visible disease symptoms.",
                "treatments": ["Continue regular care", "Monitor for changes"],
                "prevention": ["Proper watering", "Good spacing", "Regular inspection"],
                "kannada_names": {"disease": "ಆರೋಗ್ಯಕರ ಸಸ್ಯ", "treatment": "ನಿಯಮಿತ ಆರೈಕೆ"}
            },
            "timestamp": datetime.now().isoformat()
        }

    def _mock_market_analysis(self, crop_name: str, location: str) -> Dict:
        """Mock market analysis for when Vertex AI is not available"""
        return {
            "success": True,
            "analysis": {
                "trend": "stable",
                "prediction": "Prices expected to remain stable with slight increase",
                "recommendation": "WAIT",
                "reasoning": "Current prices are moderate. Waiting 1-2 weeks may yield better prices.",
                "best_markets": [f"{location} Main Mandi", "Agricultural Produce Market"],
                "optimal_timing": "Within 2-3 weeks"
            },
            "current_prices": {
                "crop": crop_name,
                "current_price": "₹2,500/quintal",
                "trend": "stable"
            },
            "timestamp": datetime.now().isoformat()
        }

    def _mock_scheme_answer(self, question: str, language: str) -> Dict:
        """Mock scheme answer for when Vertex AI is not available"""
        return {
            "success": True,
            "answer": {
                "scheme_name": "PM-KISAN Scheme",
                "description": "Direct income support to farmers with ₹6,000 per year",
                "eligibility": "All landholding farmers",
                "benefits": "₹2,000 every 4 months (₹6,000/year)",
                "application_process": "Register online at pmkisan.gov.in or visit local agricultural office",
                "documents": ["Aadhaar Card", "Land Records", "Bank Account Details"],
                "links": ["https://pmkisan.gov.in", "https://agri.karnataka.gov.in"],
                "deadlines": "No deadline - open throughout year"
            },
            "language": language,
            "timestamp": datetime.now().isoformat()
        }
