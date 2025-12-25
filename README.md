# hinthint
from flask import Flask, request, render_template_string

app = Flask(__name__)

# 사건 관련 데이터 (질문에 답변하는 AI용)
data = {
    "범행 특징": "숭례문 전소 사건은 국가와 사회 시스템에 대한 불만과 계획적 행동이 결합된 사건입니다.",
    "용의자": "주요 용의자는 최수진, 소방관이며 특정 정보는 힌트로 제공됩니다.",
    "방법": "화재 진압 지연, 내부 구조 이해, 최소한의 행동으로 최대 효과를 노린 계획적 범행.",
    "동기": "직업적 좌절, 개인적 고통, 사회 시스템에 대한 분노가 결합된 사례입니다."
}

# 힌트 관리
hint_count = 0
max_hints = 2
hints = [
    "힌트1: 진범은 소방관이며, 특수한 상황(임신)과 직업 지식이 결합되어 계획적 범행을 수행했습니다.",
    "힌트2: 진범의 범행은 사회적 불만과 개인적 고통을 표현하는 방식으로 숭례문을 표적으로 삼았습니다."
]

# HTML 템플릿
HTML_PAGE = '''
<!doctype html>
<title>Hint AI</title>
<h2>질문을 입력하세요 (힌트 2회 제공)</h2>
<form action="/" method="post">
  <input name="user_input" style="width: 400px">
  <input type="submit" value="질문">
</form>
<h3>답변:</h3>
<p>{{ answer }}</p>
<h3>사용한 힌트:</h3>
<ul>
{% for h in used_hints %}
  <li>{{ h }}</li>
{% endfor %}
</ul>
'''

used_hints = []

@app.route("/", methods=["GET", "POST"])
def home():
    global hint_count
    answer = "질문을 입력하세요."
    if request.method == "POST":
        user_input = request.form["user_input"].lower()
        answer = ""

        # 단어 기반 답변
        matched = False
        for key, val in data.items():
            if key in user_input or any(word in user_input for word in key.split()):
                answer = val
                matched = True
                break

        # 힌트 제공 조건
        if not matched:
            if hint_count < max_hints:
                hint = hints[hint_count]
                answer = f"단서 이해가 어렵다면 힌트를 확인하세요: {hint}"
                used_hints.append(hint)
                hint_count += 1
            else:
                answer = "질문을 더 분석할 수 없습니다. 힌트 사용 횟수는 모두 소진되었습니다."

    return render_template_string(HTML_PAGE, answer=answer, used_hints=used_hints)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
