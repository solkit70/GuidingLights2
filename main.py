import streamlit as st
from langchain_openai import ChatOpenAI
from openai import OpenAIError, Image
from datetime import datetime
from openai import OpenAI
from langchain_community.callbacks import get_openai_callback

# Function to interact with OpenAI API
def generate_text(api_key, birth_date, gender, language):
    try: 
        model_name = "gpt-4o-mini"
        llm = ChatOpenAI(openai_api_key=api_key, model_name=model_name)

        current_year = datetime.now().year
        birth_year = int(birth_date.split("년")[0])
        age = current_year - birth_year
        age_group = (age // 10) * 10

        if age_group == 10:
            age_advice = "🧒 이 시기는 자신을 찾는 여행의 시작입니다. 두려워하지 말고 실수 속에서도 당신을 사랑하세요."
        elif age_group == 20:
            age_advice = "👩‍🎓 실패는 성장의 자양분입니다. 용기를 내어 새로운 도전을 하세요."
        elif age_group in [30, 40]:
            age_advice = "👨‍👩‍👧‍👦 가정과 일 사이에서 때로는 지치고, 스스로를 잊을 수 있지만, 당신은 이미 잘 해내고 있습니다."
        else:
            age_advice = "🧑‍🦳 이제 인생의 깊이를 느낄 때입니다. 지난 길을 자랑스러워 하세요."

        instruction = f"""
        당신은 따뜻한 조언을 주는 인생 상담자입니다. 
        {birth_date}에 태어난 {gender}의 사용자는 현재 {age}세입니다. 
        그의 현재 나이에 어울리는 따뜻한 조언, 위로, 격려의 말을 해 주세요.

        1️⃣ **나이와 기본 정보**  
        - 사용자의 나이: {age}세  
        2️⃣ **현재 나이에 어울리는 조언**  
        - {age_advice}  
        3️⃣ **구체적인 행동 계획**  
        - 건강 관리, 자기 계발, 인간관계 강화, 재정 계획 등 구체적인 행동 계획을 제안해 주세요.  
        4️⃣ **위로와 격려의 말**  
        - 답변에 이모티콘(Emoji)을 사용하여 가독성을 높여 주세요. 😊  
        """
        query = instruction + ". 대답은 " + language + "로 해 주세요."

        with get_openai_callback() as cb:
            generated_text = llm.invoke(query)
            st.write(cb)
        return generated_text
    except OpenAIError as e:
        st.warning("Incorrect API key provided or OpenAI API error. You can find your API key at https://platform.openai.com/account/api-keys.")

# Function to generate an image based on the response content
def generate_image(api_key, prompt, age_group, language):
    try:
        if age_group == 10:
            theme = "a cheerful cartoon character popular among teenagers"
        elif age_group == 20:
            theme = "a nostalgic character from the 2000s"
        elif age_group in [30, 40]:
            theme = "a classic character from the 1980s or 1990s"
        else:
            theme = "a timeless character from the 1960s or 1970s"

        if language == "Korean":
            theme += ", such as Pororo or Dooly, in a bright and hopeful setting inspired by South Korea"
        elif language == "Japanese":
            theme += ", such as Doraemon or Astro Boy, in a peaceful and inspiring scene inspired by Japan"
        elif language == "English":
            theme += ", such as Mickey Mouse or Snoopy, in a joyful and uplifting environment"
        elif language == "French":
            theme += ", such as Tintin or Asterix, in a charming and adventurous setting inspired by France"
        elif language == "Spanish":
            theme += ", such as Mafalda or Don Quixote, in a warm and optimistic atmosphere"
        else:
            theme += ", inspired by popular characters and cultural elements from the selected language"

        full_prompt = f"Create an illustration that visually represents the following advice: {prompt}. Avoid using text in the image. Focus on {theme}."

        client = OpenAI(api_key=api_key)
        response = client.images.generate(
            model="dall-e-3",
            prompt=full_prompt,
            size="1024x1024",
            quality="standard",
            n=1
        )
        return response.data[0].url
    except OpenAIError as e:
        st.warning("Error generating image. Please check your API key or try again later.")
        return None

def main():
    st.title('Guiding Light 🌟')

    api_key = st.text_input("Please input your OpenAI API Key:", type="password")
    current_year = datetime.now().year   
    birth_date = st.date_input("Select your birth date", min_value=datetime(1900, 1, 1), max_value=datetime(current_year, 12, 31), format="MM/DD/YYYY")
    year = str(birth_date.year)
    month = str(birth_date.month)
    day = str(birth_date.day)   
    birth_date_str = year + "년 " + month + "월 " + day + "일"    
    gender = st.radio("Select your gender", ["Male", "Female"])
    available_languages = [
        "English", "Korean", "Spanish", "French", "German", "Chinese", "Japanese",
        "Italian", "Portuguese", "Russian", "Arabic", "Hindi", "Dutch", "Swedish", "Turkish"
    ]
    selected_language = st.selectbox("Select a language:", available_languages)  

    if st.button("Shine My Day"):
        if api_key:
            with st.spinner('Wait for it...'):    
                generated_text = generate_text(api_key, birth_date_str, gender, selected_language)
                st.write("Generated counsel:")
                st.write(generated_text.content)

                image_prompt = f"A bright and hopeful illustration inspired by the following advice: {generated_text.content}"
                birth_year = int(birth_date.year)
                age_group = ((current_year - birth_year) // 10) * 10
                image_url = generate_image(api_key, image_prompt, age_group, selected_language)
                if image_url:
                    st.image(image_url, caption="Generated Image")
        else:
            st.warning("Please insert your OpenAI API key.")

if __name__ == "__main__":
    main()
