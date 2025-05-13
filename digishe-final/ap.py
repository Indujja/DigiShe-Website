from flask import Flask, render_template, request
import pandas as pd

ap = Flask(__name__)

data = pd.read_csv("data.csv")  # Ensure this file exists

@ap.route('/')
def index():
    return render_template("frontend.html")

@ap.route('/get', methods=['POST'])
def get_response():
    user_query = request.form['msg']
    language = request.form.get('lang', 'en')
    
    # Filter dataset based on the user query
    filtered_data = data[data['Scheme Name'].str.contains(user_query, case=False, na=False)]
    
    responses = {
        "en": "Sorry, no schemes matched your query. Please try another keyword.",
        "hi": "माफ करें, आपकी खोज से कोई योजना मेल नहीं खाती। कृपया एक और कीवर्ड आज़माएं।",
        "kn": "ಕ್ಷಮಿಸಿ, ನಿಮ್ಮ ಪ್ರಶ್ನೆಗೆ ಯಾವುದೇ ಯೋಜನೆಗಳು ಹೊಂದಿಕೆಯಾಗುತ್ತಿಲ್ಲ. ದಯವಿಟ್ಟು ಮತ್ತೊಂದು ಕೀವರ್ಡ್ ಪ್ರಯತ್ನಿಸಿ.",
        "ta": "மன்னிக்கவும், உங்கள் தேடலுக்கு பொருத்தமான திட்டங்கள் இல்லை. தயவுசெய்து வேறொரு முக்கிய வார்த்தையை முயற்சிக்கவும்.",
        "te": "క్షమించండి, మీ ప్రశ్నకు సరిపోయే పథకాలు లేవు. దయచేసి మరొక కీవర్డ్ ప్రయత్నించండి.",
        "bn": "দুঃখিত, আপনার অনুসন্ধানের সাথে কোনও প্রকল্প মেলেনি। অনুগ্রহ করে অন্য কীওয়ার্ড চেষ্টা করুন।"
    }
    
    if filtered_data.empty:
        return responses.get(language, responses["en"])
    
    result_templates = {
        "en": "Here are the schemes that match your query:<br>",
        "hi": "ये योजनाएँ आपकी खोज से मेल खाती हैं:<br>",
        "kn": "ಇವು ನಿಮ್ಮ ಪ್ರಶ್ನೆಗೆ ಹೊಂದಿಕೊಳ್ಳುವ ಯೋಜನೆಗಳು:<br>",
        "ta": "இவை உங்கள் தேடலுடன் பொருந்தும் திட்டங்கள்:<br>",
        "te": "ఇవి మీ ప్రశ్నకు సరిపోయే పథకాలు:<br>",
        "bn": "এগুলি আপনার অনুসন্ধানের সাথে মিলিত প্রকল্পগুলি:<br>"
    }
    
    response_text = result_templates.get(language, result_templates["en"])
    
    for _, row in filtered_data.iterrows():
        response_text += f"<b>{row['Scheme Name']}</b><br>URL: <a href='{row['URL']}' target='_blank'>{row['URL']}</a><br><br>"
    
    return response_text

if __name__ == "__main__":
    ap.run(debug=True)
