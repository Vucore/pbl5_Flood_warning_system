import re
import json
import random
import numpy as np
from typing import Dict, Any, Optional, List, Tuple
from datetime import datetime

# Load responses from the JSON file
json_path = "services/responses.json"
try:
    with open(json_path, 'r', encoding='utf-8') as f:
        RESPONSES = json.load(f)
        print(f"Loading responses.json Success!")
except (FileNotFoundError, json.JSONDecodeError) as e:
    print(f"Error loading responses.json: {e}")
    # Fallback minimal responses
    RESPONSES = {
        "en": {
            "greetings": ["Hello! How can I help you?"],
            "farewell": ["Goodbye!"],
            "thanks": ["You're welcome!"],
            "unknown": ["I don't understand that question."],
            "flood_info": ["Flooding occurs when water overflows onto land."],
            "warning_levels": ["We have four warning levels."],
            "safety_tips": ["Stay safe during floods."]
        },
        "vi": {
            "greetings": ["Xin chào! Tôi có thể giúp gì cho bạn?"],
            "farewell": ["Tạm biệt!"],
            "thanks": ["Không có gì!"],
            "unknown": ["Tôi không hiểu câu hỏi đó."],
            "flood_info": ["Lũ lụt xảy ra khi nước tràn vào đất liền."],
            "warning_levels": ["Chúng tôi có bốn cấp cảnh báo."],
            "safety_tips": ["Hãy đảm bảo an toàn trong lũ lụt."]
        }
    }

# Keywords for intent recognition
KEYWORDS = {
    "greeting": ["hello", "hi", "hey", "greetings", "xin chào", "chào", "good morning", "good afternoon"],
    "farewell": ["bye", "goodbye", "see you", "tạm biệt", "hẹn gặp lại"],
    "thanks": ["thank", "thanks", "appreciate", "cảm ơn", "cám ơn", "biết ơn"],
    "risk_level": ["risk", "danger", "warning", "level", "status", "nguy hiểm", "cảnh báo", "nguy cơ", "trạng thái", "tình trạng"],
    "prediction": ["predict", "forecast", "future", "tomorrow", "later", "dự báo", "dự đoán", "tương lai", "ngày mai", "sau này", "will it flood", "có lũ không"],
    "sensor_data": ["temperature", "pressure", "humidity", "rainfall", "water", "soil", "nhiệt độ", "áp suất", "độ ẩm", "lượng mưa", "nước", "đất", "reading", "sensor", "cảm biến", "số liệu"],
    "current_situation": ["current", "now", "happening", "current situation", "tình hình hiện tại", "hiện tại", "bây giờ", "đang xảy ra", "situation now", "what's happening", "show me data", "hiển thị dữ liệu", "tell me about current", "how is it now"],
    "flood_info": ["what is flood", "about flood", "flood information", "lũ lụt là gì", "về lũ lụt", "thông tin lũ lụt", "explain flood", "cause", "nguyên nhân"],
    "warning_levels": ["warning level", "alert level", "warning system", "cấp độ cảnh báo", "hệ thống cảnh báo", "mức độ cảnh báo", "alert system"],
    "safety_tips": ["safe", "safety", "protect", "prepare", "action", "an toàn", "bảo vệ", "chuẩn bị", "hành động", "what to do", "làm gì", "emergency", "khẩn cấp"]
}

def extract_intent(message: str) -> str:
    """
    Extract the primary intent from a user message using keyword matching.
    Now with improved language understanding.
    
    Args:
        message: The user's message
        
    Returns:
        The identified intent
    """
    message = message.lower()
    
    # Score each intent based on keyword matches
    intent_scores = {}
    for intent, keywords in KEYWORDS.items():
        score = 0
        for keyword in keywords:
            if keyword in message:
                # Exact matches get higher scores
                if f" {keyword} " in f" {message} ":
                    score += 2
                else:
                    score += 1
        intent_scores[intent] = score
    
    # Check for prediction requests specifically
    # prediction_patterns = [
    #     r"(will|is).*(flood|flooding).*\?",
    #     r"(có|sẽ).*ngập.*\?",
    #     r"(có|sẽ).*lũ.*\?",
    #     r"(predict|forecast|dự báo|dự đoán).*([0-9]+.*hour|day|giờ|ngày)"
    # ]
    
    # for pattern in prediction_patterns:
    #     if re.search(pattern, message):
    #         intent_scores["prediction"] += 3
    
    # Find the intent with the highest score
    max_score = 0
    best_intent = "unknown"
    
    for intent, score in intent_scores.items():
        if score > max_score:
            max_score = score
            best_intent = intent
    
    # If we have a very low confidence, return unknown
    if max_score < 1:
        return "unknown"
    
    return best_intent


def process_message(message: str, language: str, latest_data: Optional[Any], warning_level: str) -> str:
    """
    Process a user message and generate a response.
    
    Args:
        message: The user's message
        language: The current language (en or vi)
        latest_data: The latest sensor data (if available)
        warning_level: The current warning level
        translations: Dictionary of translations
        
    Returns:
        The chatbot's response
    """
    intent = extract_intent(message)
    
    # Get translations for the current language
    # trans = translations.get(language, translations["en"])
    lang = language
    
    # Handle each intent
    if intent == "greeting":
        return random.choice(RESPONSES[lang]["greetings"])
    
    elif intent == "farewell":
        return random.choice(RESPONSES[lang]["farewell"])
    
    elif intent == "thanks":
        return random.choice(RESPONSES[lang]["thanks"])
    
    elif intent == "risk_level":
        if latest_data is None:
            if language == "en":
                return "I don't have any current sensor data to assess risk levels."
            else:
                return "Tôi không có dữ liệu cảm biến hiện tại để đánh giá mức độ rủi ro."
        
        # level_name = trans[warning_level]
        # level_message = trans[f"{warning_level}_message"]

        level_name = warning_level
        level_message = "Một số thông số cho thấy nguy cơ tiềm ẩn. Theo dõi tình hình."
        
        if language == "en":
            return f"The current flood risk level is: {level_name}. {level_message}"
        else:
            return f"Mức độ rủi ro lũ lụt hiện tại là: {level_name}. {level_message}"
    
    elif intent == "sensor_data":      
        if latest_data is None:
            if language == "en":
                return "I don't have any current sensor data available."
            else:
                return "Tôi không có dữ liệu cảm biến hiện tại."
        
        if language == "en":
            return (f"Current sensor readings:\n"
                   f"• Temperature: {latest_data['temperature']}°C\n"
                   f"• Air Pressure: {latest_data['air_pressure']} hPa\n"
                   f"• Air Humidity: {latest_data['air_humidity']}%\n"
                   f"• Rainfall: {latest_data['rainfall']}\n"
                   f"• Soil Humidity: {latest_data['soil_humidity']}\n"
                   f"• Water Level: {latest_data['water_level']} cm")
        else:
            return (f"Chỉ số cảm biến hiện tại:\n"
                    f"• Hiện tại: {latest_data['timestamp']}\n"
                   f"• Nhiệt độ: {latest_data['temperature']}°C\n"
                   f"• Áp suất không khí: {latest_data['air_pressure']} hPa\n"
                   f"• Độ ẩm không khí: {latest_data['air_humidity']}%\n"
                   f"• Lượng mưa: {latest_data['rainfall']}\n"
                   f"• Độ ẩm đất: {latest_data['soil_humidity']}\n"
                   f"• Mực nước: {latest_data['water_level']} cm")
    
    # elif intent == "prediction":
    #     # Get prediction from ML model based on latest data
    #     if latest_data:
    #         # ml_warning_level, confidence = get_prediction_from_ml_model(latest_data)
    #         # confidence_percent = int(confidence * 100)
            
    #         # Analyze which factors are contributing to the risk
    #         water_level = latest_data.water_level
    #         rainfall = latest_data.rainfall
    #         soil_humidity = latest_data.soil_humidity
            
    #         # Determine which factors are most concerning
    #         critical_factors = []
    #         if water_level >= 150:
    #             critical_factors.append(("water_level", water_level))
    #         if rainfall >= 5.0:
    #             critical_factors.append(("rainfall", rainfall))
    #         if soil_humidity >= 75:
    #             critical_factors.append(("soil_humidity", soil_humidity))
            
    #         # Sort factors by severity (most critical first)
    #         critical_factors.sort(key=lambda x: x[1], reverse=True)
            
    #         # Format factor messages
    #         factor_messages = ""
    #         if critical_factors:
    #             if language == "en":
    #                 factor_messages = "\n\nKey contributing factors:"
    #                 for factor, value in critical_factors:
    #                     if factor == "water_level":
    #                         factor_messages += f"\n• Water level: {value} cm (Critical level: >150 cm)"
    #                     elif factor == "rainfall":
    #                         factor_messages += f"\n• Rainfall: {value} mm (Critical level: >5.0 mm)"
    #                     elif factor == "soil_humidity":
    #                         factor_messages += f"\n• Soil humidity: {value}% (Critical level: >75%)"
    #             else:
    #                 factor_messages = "\n\nCác yếu tố đóng góp chính:"
    #                 for factor, value in critical_factors:
    #                     if factor == "water_level":
    #                         factor_messages += f"\n• Mực nước: {value} cm (Mức độ nguy hiểm: >150 cm)"
    #                     elif factor == "rainfall":
    #                         factor_messages += f"\n• Lượng mưa: {value} mm (Mức độ nguy hiểm: >5.0 mm)"
    #                     elif factor == "soil_humidity":
    #                         factor_messages += f"\n• Độ ẩm đất: {value}% (Mức độ nguy hiểm: >75%)"
            
    #         # Only override the warning level if the ML model has high confidence
    #         # prediction_level = ml_warning_level if confidence > 0.6 else warning_level
            
    #         # Add sensor data summary
    #         if language == "en":
    #             sensor_summary = (f"\n\nCurrent readings summary:\n"
    #                            f"• Temperature: {latest_data.temperature}°C\n"
    #                            f"• Air Pressure: {latest_data.air_pressure} hPa\n"
    #                            f"• Air Humidity: {latest_data.air_humidity}%\n"
    #                            f"• Rainfall: {latest_data.rainfall} mm\n"
    #                            f"• Soil Humidity: {latest_data.soil_humidity}%\n"
    #                            f"• Water Level: {latest_data.water_level} cm")
    #         else:
    #             sensor_summary = (f"\n\nTóm tắt chỉ số hiện tại:\n"
    #                            f"• Nhiệt độ: {latest_data.temperature}°C\n"
    #                            f"• Áp suất không khí: {latest_data.air_pressure} hPa\n"
    #                            f"• Độ ẩm không khí: {latest_data.air_humidity}%\n"
    #                            f"• Lượng mưa: {latest_data.rainfall} mm\n"
    #                            f"• Độ ẩm đất: {latest_data.soil_humidity}%\n"
    #                            f"• Mực nước: {latest_data.water_level} cm")
            
    #         # if language == "en":
    #         #     if prediction_level == "normal":
    #         #         return f"Based on current data, no flooding is predicted in the near future (confidence: {confidence_percent}%).{factor_messages}{sensor_summary}\n\nContinue to monitor for updates."
    #         #     elif prediction_level == "watch":
    #         #         return f"Our models show a slight risk of flooding in the next 24-48 hours (confidence: {confidence_percent}%).{factor_messages}{sensor_summary}\n\nStay alert and monitor updates."
    #         #     elif prediction_level == "warning":
    #         #         return f"Warning: There is a significant chance of flooding within the next 24 hours (confidence: {confidence_percent}%).{factor_messages}{sensor_summary}\n\nMake preparations and stay informed."
    #         #     else:  # severe
    #         #         return f"SEVERE WARNING: Flooding is imminent or already occurring (confidence: {confidence_percent}%).{factor_messages}{sensor_summary}\n\nTake immediate action to protect yourself and your property."
    #         # else:
    #         #     if prediction_level == "normal":
    #         #         return f"Dựa trên dữ liệu hiện tại, không có dự báo lũ lụt trong tương lai gần (độ tin cậy: {confidence_percent}%).{factor_messages}{sensor_summary}\n\nTiếp tục theo dõi các cập nhật."
    #         #     elif prediction_level == "watch":
    #         #         return f"Các mô hình của chúng tôi cho thấy nguy cơ lũ lụt nhẹ trong 24-48 giờ tới (độ tin cậy: {confidence_percent}%).{factor_messages}{sensor_summary}\n\nHãy cảnh giác và theo dõi các cập nhật."
    #         #     elif prediction_level == "warning":
    #         #         return f"Cảnh báo: Có khả năng lũ lụt đáng kể trong 24 giờ tới (độ tin cậy: {confidence_percent}%).{factor_messages}{sensor_summary}\n\nHãy chuẩn bị và theo dõi thông tin."
    #         #     else:  # severe
    #         #         return f"CẢNH BÁO NGHIÊM TRỌNG: Lũ lụt sắp xảy ra hoặc đã xảy ra (độ tin cậy: {confidence_percent}%).{factor_messages}{sensor_summary}\n\nHãy thực hiện hành động ngay lập tức để bảo vệ bản thân và tài sản của bạn."
    #     else:
    #         if language == "en":
    #             return "I don't have enough data to make a flood prediction at this time."
    #         else:
    #             return "Tôi không có đủ dữ liệu để đưa ra dự đoán lũ lụt vào lúc này."
    
    elif intent == "current_situation":
        # Provide a comprehensive situation report
        if latest_data is None:
            if language == "en":
                return "I don't have current data to assess the situation."
            else:
                return "Tôi không có dữ liệu hiện tại để đánh giá tình hình."
        
    #     # Get a prediction from the ML model
    #     # ml_warning_level, confidence = get_prediction_from_ml_model(latest_data)
    #     # confidence_percent = int(confidence * 100)
        
    #     # Format situation report
    #     level_name = trans[warning_level]
    #     level_message = trans[f"{warning_level}_message"]
        
    #     # Format sensor readings
    #     if language == "en":
    #         sensor_readings = (f"Current sensor readings:\n"
    #                    f"• Temperature: {latest_data.temperature}°C\n"
    #                    f"• Air Pressure: {latest_data.air_pressure} hPa\n"
    #                    f"• Air Humidity: {latest_data.air_humidity}%\n"
    #                    f"• Rainfall: {latest_data.rainfall} mm/h\n"
    #                    f"• Soil Humidity: {latest_data.soil_humidity}%\n"
    #                    f"• Water Level: {latest_data.water_level} cm")
            
    #         # Analyze key factors contributing to current risk level
    #         factor_analysis = "\nRisk factor analysis:"
            
    #         if latest_data.water_level > 150:
    #             factor_analysis += f"\n• Water level is {latest_data.water_level} cm - ABOVE CRITICAL THRESHOLD (150 cm)"
    #         elif latest_data.water_level > 135:
    #             factor_analysis += f"\n• Water level is {latest_data.water_level} cm - above warning threshold (135 cm)"
    #         else:
    #             factor_analysis += f"\n• Water level is {latest_data.water_level} cm - within safe range"
                
    #         if latest_data.rainfall > 5.0:
    #             factor_analysis += f"\n• Rainfall is {latest_data.rainfall} mm/h - ABOVE CRITICAL THRESHOLD (5.0 mm/h)"
    #         elif latest_data.rainfall > 2.5:
    #             factor_analysis += f"\n• Rainfall is {latest_data.rainfall} mm/h - above warning threshold (2.5 mm/h)"
    #         else:
    #             factor_analysis += f"\n• Rainfall is {latest_data.rainfall} mm/h - within safe range"
                
    #         if latest_data.soil_humidity > 75:
    #             factor_analysis += f"\n• Soil humidity is {latest_data.soil_humidity}% - ABOVE CRITICAL THRESHOLD (75%)"
    #         elif latest_data.soil_humidity > 60:
    #             factor_analysis += f"\n• Soil humidity is {latest_data.soil_humidity}% - above warning threshold (60%)"
    #         else:
    #             factor_analysis += f"\n• Soil humidity is {latest_data.soil_humidity}% - within safe range"
            
    #         return (f"Current situation report:\n\n"
    #                f"Warning level: {level_name} - {level_message}\n\n"
    #                f"{sensor_readings}\n"
    #                f"{factor_analysis}\n\n")
    #             #    f"ML model prediction confidence: {confidence_percent}%")
    #     else:
    #         sensor_readings = (f"Chỉ số cảm biến hiện tại:\n"
    #                    f"• Nhiệt độ: {latest_data.temperature}°C\n"
    #                    f"• Áp suất không khí: {latest_data.air_pressure} hPa\n"
    #                    f"• Độ ẩm không khí: {latest_data.air_humidity}%\n"
    #                    f"• Lượng mưa: {latest_data.rainfall} mm/h\n"
    #                    f"• Độ ẩm đất: {latest_data.soil_humidity}%\n"
    #                    f"• Mực nước: {latest_data.water_level} cm")
            
    #         # Analyze key factors contributing to current risk level
    #         factor_analysis = "\nPhân tích yếu tố rủi ro:"
            
    #         if latest_data.water_level > 150:
    #             factor_analysis += f"\n• Mực nước là {latest_data.water_level} cm - VƯỢT QUÁ NGƯỠNG NGUY HIỂM (150 cm)"
    #         elif latest_data.water_level > 135:
    #             factor_analysis += f"\n• Mực nước là {latest_data.water_level} cm - vượt quá ngưỡng cảnh báo (135 cm)"
    #         else:
    #             factor_analysis += f"\n• Mực nước là {latest_data.water_level} cm - trong phạm vi an toàn"
                
    #         if latest_data.rainfall > 5.0:
    #             factor_analysis += f"\n• Lượng mưa là {latest_data.rainfall} mm/h - VƯỢT QUÁ NGƯỠNG NGUY HIỂM (5.0 mm/h)"
    #         elif latest_data.rainfall > 2.5:
    #             factor_analysis += f"\n• Lượng mưa là {latest_data.rainfall} mm/h - vượt quá ngưỡng cảnh báo (2.5 mm/h)"
    #         else:
    #             factor_analysis += f"\n• Lượng mưa là {latest_data.rainfall} mm/h - trong phạm vi an toàn"
                
    #         if latest_data.soil_humidity > 75:
    #             factor_analysis += f"\n• Độ ẩm đất là {latest_data.soil_humidity}% - VƯỢT QUÁ NGƯỠNG NGUY HIỂM (75%)"
    #         elif latest_data.soil_humidity > 60:
    #             factor_analysis += f"\n• Độ ẩm đất là {latest_data.soil_humidity}% - vượt quá ngưỡng cảnh báo (60%)"
    #         else:
    #             factor_analysis += f"\n• Độ ẩm đất là {latest_data.soil_humidity}% - trong phạm vi an toàn"
            
    #         return (f"Báo cáo tình hình hiện tại:\n\n"
    #                f"Mức cảnh báo: {level_name} - {level_message}\n\n"
    #                f"{sensor_readings}\n"
    #                f"{factor_analysis}\n\n")
    #             #    f"Độ tin cậy của mô hình dự đoán: {confidence_percent}%")
    
    elif intent == "flood_info":
        return random.choice(RESPONSES[lang]["flood_info"])
    
    elif intent == "warning_levels":
        return random.choice(RESPONSES[lang]["warning_levels"])
    
    elif intent == "safety_tips":
        # Customize safety tips based on current warning level
        tips = random.choice(RESPONSES[lang]["safety_tips"])
        if language == "en":
            return f"Safety tips for current {warning_level} level:\n{tips}"
        else:
            return f"Lời khuyên an toàn cho mức {warning_level} hiện tại:\n{tips}"
    
    else:  # unknown intent
        return random.choice(RESPONSES[lang]["unknown"])
