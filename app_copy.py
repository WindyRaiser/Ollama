# Flask: Python으로 웹 애플리케이션을 구축할 수 있게 해주는 프레임워크입니다.
# openai: OpenAI API를 사용해 GPT 모델을 호출하기 위한 라이브러리입니다.
import os
from flask import Flask, render_template, request
import openai
from dotenv import load_dotenv

# OpenAI API Key 설정
# OpenAI API에 접근하기 위해서 인증에 필요한 API 키를 설정합니다. 
# 중요: 실제로는 API 키를 소스코드에 직접 넣지 않고, 환경 변수로 설정하는 것이 안전합니다.

load_dotenv()

# 환경 변수에서 API 키 가져오기
openai.api_key = os.getenv("OPENAI_API_KEY")

# Flask 객체를 생성하여 애플리케이션을 초기화합니다. __name__은 현재 모듈의 이름을 전달하는데, 
# Flask가 이 정보를 바탕으로 템플릿 및 기타 자원을 찾습니다.
app = Flask(__name__)

# / 경로에 접근하면 index.html 파일을 렌더링합니다. 사용자가 웹사이트에 처음 접속했을 때 이 함수가 호출됩니다.
# index.html은 기본 질문 입력 화면을 구성할 HTML 템플릿 파일입니다.
@app.route('/')
def index():
    return render_template('index.html')

# /ask 경로로 POST 요청을 받으면 이 함수가 호출됩니다.
# 사용자가 입력한 질문은 HTML 폼을 통해 전달되며, request.form['question']을 통해 해당 질문을 가져옵니다.

@app.route('/ask', methods=['POST'])
def ask():
    question = request.form['question']

# OpenAI의 ChatCompletion.create 메서드를 호출하여 GPT-3.5 Turbo 모델을 사용해 응답을 생성합니다.
# messages는 대화 흐름을 전달하는 역할을 하며, role은 system과 user로 나뉩니다. 여기서 system은 AI의 역할을 지정하는 메시지, user는 사용자의 질문입니다.
# max_tokens=100은 생성되는 응답의 최대 토큰 수를 100으로 제한합니다. 토큰은 텍스트의 단위이며, 하나의 토큰은 대략 4문자 또는 0.75 단어에 해당합니다.
    # 최신 GPT-3.5 Turbo 모델을 사용하여 응답 생성

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": question}
        ],
        max_tokens=300
    )

# GPT 모델의 응답은 response['choices'][0]['message']['content']에서 가져옵니다.
# strip()을 사용하여 앞뒤의 불필요한 공백을 제거합니다.
    answer = response['choices'][0]['message']['content'].strip()

# index.html을 다시 렌더링하면서, 사용자가 입력한 질문(question)과 GPT 모델의 응답(answer)을 함께 넘겨줍니다. 
# 이렇게 하면 질문과 응답이 같은 페이지에 표시됩니다.
    return render_template('index.html', question=question, answer=answer)

# 이 코드는 Python 파일이 직접 실행될 때 Flask 애플리케이션을 실행합니다.
# debug=True는 디버깅 모드를 활성화하는데, 코드 변경 시 자동으로 서버를 재시작하고 에러 메시지를 더 자세히 표시합니다.

if __name__ == '__main__':
    app.run(debug=True)
