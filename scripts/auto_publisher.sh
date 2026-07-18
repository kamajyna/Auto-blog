#!/bin/bash

# 설정: 블로그 디렉토리 경로
BLOG_DIR="/Users/kongjiyun/auto-blog"
cd $BLOG_DIR || exit

# 가상환경 활성화 (필요한 경우)
# source scripts/venv/bin/activate

# 1. 새 블로그 포스트 생성 (Python 스크립트 실행)
echo "Generating new blog post..."
# export GEMINI_API_KEY="your_api_key_here" # 환경변수로 설정 필요
python3 scripts/auto_blogger.py

# 2. Git에 반영 및 Push
echo "Committing and pushing to GitHub..."
git add _posts/
git commit -m "Auto-published post: $(date +'%Y-%m-%d %H:%M:%S')"
git push origin main

echo "Done!"
