from flask import Flask, request, render_template_string
import os

app = Flask(__name__)

# 힌트 사용 횟수
hints_total = 2
hints_left = hints_total

# 단서 데이터
clues = [
    "범행 장소와 관련된 중요한 직업적 지식이 활용되었음.",
    "개인의 불만과 사회 시스템에 대한 배신감이 행동에 영향을 줌."
]

# HTML 템플릿 (하나로 통합)
html_template = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>힌트 AI</title>
</head>
<body>
    <h1>힌트 AI</h1>
    <form action="/" method="post">
        <label for="question">질문을 입력하세요:</label><br>
        <input type="text" id="question" name="question" size="50"><br><br>
        <input type="submit" value="질문">
    </form>
    <p><strong>답변:</strong> {{ answer }}</p>
    <p><strong>남은 힌트:</strong> {{ hints_left }}</p>
</body>
</html>
"""

def generate_answer(question):
    global hints_left
    question_lower = question.lower()
    
    # 힌트 요청 시
    if "힌트" in question_lower or "단서" in question_lower:
        if hints_left > 0:
            hints_left -= 1
            return clues[hints_total - hints_left - 1]
        else:
            return "힌트를 모두 사용했습니다."
    
    # 질문 내용 분석 후 답변
    if "동기" in question_lower:
        return "범행의 동기는 사건과 관련된 개인적 좌절과 사회적 문제와 연결되어 있습니다."
    elif "방법" in question_lower or "수법" in question_lower:
        return "범행은 해당 사건과 관련된 전문 지식을 활용한 계획적 수법입니다."
    else:
        return "질문 내용을 바탕으로 분석 중입니다. 필요 시 '힌트'를 요청하세요."

@app.route("/", methods=["GET", "POST"])
def index():
    global hints_left
    answer = ""
    if request.method == "POST":
        question = request.form.get("question")
        answer = generate_answer(question)
    return render_template_string(html_template, answer=answer, hints_left=hints_left)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
