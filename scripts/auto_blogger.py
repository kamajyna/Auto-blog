import os
import datetime
import random
from google import genai
from google.genai import types

def get_daily_topic():
    # 리스크가 적고 트래픽이 꾸준한 주제(Evergreen niche) 풀
    topics = [
        "직장인을 위한 구글 스프레드시트 꿀팁",
        "애플 실리콘 맥북 배터리 관리 최적화 방법",
        "노션(Notion)으로 개인 일정 관리하는 법",
        "AI 챗봇을 업무에 활용하는 3가지 방법",
        "초보자를 위한 인덱스 펀드 투자 기본 개념",
        "눈 건강을 지키는 스마트폰 다크모드 활용법"
    ]
    return random.choice(topics)

def generate_blog_post(topic):
    # Gemini API 키 확인
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("GEMINI_API_KEY 환경변수가 설정되지 않았습니다.")
        
    client = genai.Client(api_key=api_key)
    
    prompt = f"""
당신은 IT/테크 및 생산성 향상 팁을 전문으로 다루는 파워 블로거입니다.
다음 주제에 대해 SEO에 최적화된 블로그 포스트를 작성해주세요.

주제: {topic}

요구사항:
1. 매력적이고 클릭을 유도하는 제목을 작성할 것
2. 서론, 본론(3가지 이상의 팁이나 방법), 결론으로 구조화할 것
3. 마크다운 형식으로 작성할 것 (제목은 #, 소제목은 ## 사용)
4. 본문 마지막에는 자연스럽게 관련 도서나 기기를 추천하는 문장을 넣고, [관련 상품 알아보기](https://coupa.ng/example) 링크를 삽입할 것. 
5. 그 아래에 "*(이 포스팅은 파트너스 활동의 일환으로, 이에 따른 일정액의 수수료를 제공받습니다.)*" 문구를 이탤릭체로 반드시 포함할 것.
6. 응답은 Frontmatter (layout, title, date, categories)를 포함한 완벽한 Jekyll markdown 파일 내용이어야 합니다.
7. 마크다운 코드블록(```markdown)으로 감싸지 말고 순수 텍스트만 출력하세요.

Frontmatter 예시:
---
layout: post
title: "생성된 매력적인 제목"
date: YYYY-MM-DD HH:MM:SS +0900
categories: tech
---

내용...
"""

    response = client.models.generate_content(
        model='gemini-2.5-flash',
        contents=prompt,
        config=types.GenerateContentConfig(
            temperature=0.7,
        )
    )
    
    return response.text.strip()

def save_post(content):
    # Jekyll posts 디렉토리 경로 설정
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    posts_dir = os.path.join(base_dir, "_posts")
    os.makedirs(posts_dir, exist_ok=True)
    
    now = datetime.datetime.now()
    date_str = now.strftime("%Y-%m-%d")
    
    # 임의의 슬러그 생성 (한글 제목 대신 타임스탬프 또는 순번 활용)
    slug = f"auto-post-{now.strftime('%H%M%S')}"
    filename = f"{date_str}-{slug}.md"
    filepath = os.path.join(posts_dir, filename)
    
    # 마크다운 파일 저장
    # 만약 LLM 응답이 ```markdown 으로 시작한다면 제거
    if content.startswith("```markdown"):
        content = content[11:]
    if content.startswith("```"):
        content = content[3:]
    if content.endswith("```"):
        content = content[:-3]
        
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content.strip())
        
    print(f"새 포스트가 생성되었습니다: {filepath}")
    return filepath

if __name__ == "__main__":
    try:
        print("1. 주제 선정 중...")
        topic = get_daily_topic()
        print(f"선정된 주제: {topic}")
        
        print("2. 블로그 포스트 생성 중... (Gemini API 호출)")
        post_content = generate_blog_post(topic)
        
        print("3. 포스트 저장 중...")
        save_post(post_content)
        
        print("작업 완료!")
    except Exception as e:
        print(f"오류 발생: {e}")
