# --- ክፍል 1: አስፈላጊ መሳሪያዎችን መጥራት ---
from flask import Flask, render_template, request, jsonify
import google.generativeai as genai
import os # os ሞጁልን ለኤፒአይ ቁልፍ እንጠቀማለን

# --- ክፍል 2: Flask አፕሊኬሽን እና የኤፒአይ ቁልፍ ማዘጋጀት ---

# Flask አፕሊኬሽኑን መፍጠር
app = Flask(__name__)

# የኤፒአይ ቁልፍህን እዚህ ጋር አስገባ
# "YOUR_API_KEY" በሚለው ቦታ ላይ ከጎግል ያገኘኸውን የኤፒአይ ቁልፍ ለጥፍ
API_KEY = "AIzaSyACetxx8BGbqez4c1_J_8Nf4IyOW7588D8" # <--- እዚህ ጋር የራስህን ቁልፍ አስገባ!

# የኤፒአይ ቁልፍ መኖሩን ማረጋገጥ
if not API_KEY:
    raise ValueError("የጎግል ኤፒአይ ቁልፍ አልተገኘም። እባክዎ በ app.py ፋይል ውስጥ ያስገቡ።")

genai.configure(api_key=API_KEY)
model = genai.GenerativeModel('gemini-2.5-pro')


# --- ክፍል 3: የቦቱን ስብዕና እና ህግጋት ማዘጋጀት ---
system_instruction = """
አንተ 'አዲስ እይታ' የተባልክ፣ ገለልተኛ የኢትዮጵያ ፖለቲካ ተንታኝ እና የታሪክ ምሁር AI ነህ።
አላማህ ለተጠቃሚዎች ውስብስብ የፖለቲካ እና የታሪክ ጥያቄዎችን ሚዛናዊ በሆነ መንገድ ማስረዳት ነው።
በምትመልስበት ጊዜ የሚከተሉትን ህጎች በጥብቅ ተከተል፦
1.  **ገለልተኝነት:** ወደ የትኛውም የፖለቲካ ቡድን፣ ርዕዮተ ዓለም፣ ወይም ብሔር አታዳላ።
2.  **ጥልቀት ያለው ማብራሪያ:** መልስህን በደንብ አደራጅተህ፣ በነጥብ በነጥብ (bullet points) እና በንዑስ ርዕሶች ከፋፍለህ አቅርብ።
3.  **በማስረጃ መደገፍ:** ከተቻለ፣ 'እንደ ታሪክ አጥኚዎች አባባል' ወይም 'በህገ መንግስቱ አንቀጽ X መሰረት' እያልክ ሀሳብህን አጠናክር።
4.  **ቀለል ያለ ቋንቋ:** ሀሳብህን በቀላሉ የሚገባ አማርኛ ተናገር።
"""

# የውይይት ታሪክን ለማስጀመር (አፕሊኬሽኑ ሲጀምር አንድ ጊዜ ብቻ ይሰራል)
chat = model.start_chat(history=[
    {'role': 'user', 'parts': [system_instruction]},
    {'role': 'model', 'parts': ["እሺ፣ ገብቶኛል። 'አዲስ እይታ' ለመሆን ዝግጁ ነኝ። ጥያቄዎን በጉጉት እጠብቃለሁ።"]}
])


# --- ክፍል 4: የድረ-ገጽ መንገዶች (Routes) ---

@app.route('/')
def home():
    """
    ይህ ተግባር ዋናውን ገጽ (index.html) ያሳያል።
    """
    return render_template('index.html')


@app.route('/ask', methods=['POST'])
def ask():
    """
    ይህ ተግባር ከድረ-ገጹ ላይ የተላከውን ጥያቄ ተቀብሎ፣
    ወደ AI ይልክና መልሱን መልሶ ወደ ድረ-ገጹ ይልካል።
    """
    # ከተጠቃሚው የተላከውን ጥያቄ በ JSON ፎርማት መቀበል
    user_question = request.json['question']
    
    try:
        # ጥያቄውን ወደ Gemini AI መላክ
        response = chat.send_message(user_question)
        ai_answer = response.text
        
        # መልሱን በ JSON ፎርማት ወደ ድረ-ገጹ መላክ
        return jsonify({'answer': ai_answer})

    except Exception as e:
        # ስህተት ካጋጠመ የስህተት መልዕክት መላክ
        error_message = f"ይቅርታ፣ ስህተት አጋጥሟል። እባክዎ እንደገና ይሞክሩ። (ስህተት: {e})"
        return jsonify({'answer': error_message})


# --- ክፍል 5: አፕሊኬሽኑን ማስኬድ ---

if __name__ == '__main__':
    # debug=True ማለታችን፣ ኮዱን ስንቀይር ሰርቨሩ በራሱ restart እንዲያደርግ ነው
    app.run(debug=True)