from openai import OpenAI
from sklearn.metrics.pairwise import cosine_similarity
from books.models import Book, BookRecommendation
import numpy as np
from django.conf import settings

# Upstage API 클라이언트 설정
client = OpenAI(
    api_key=settings.UPSTAGE_API_KEY,
    base_url="https://api.upstage.ai/v1/solar"
)

def recommend_books(base_title, top_n=6, base_book_id=None):
    base_book = Book.objects.filter(title__icontains=base_title).first()
    if not base_book:
        return []

    # ✅ 1. 기존 추천 캐시 있으면 바로 반환
    cached = BookRecommendation.objects.filter(base_book=base_book).first()
    if cached:
        print("[INFO] 캐시된 추천 결과 반환")
        return list(cached.recommended_books.all()[:top_n])

    # ✅ 2. 추천 계산 시작
    if base_book_id:
        try:
            base_book = Book.objects.get(pk=base_book_id)
            category = base_book.category
            all_books = list(Book.objects.filter(category=category))
        except Book.DoesNotExist:
            return []
    else:
        all_books = list(Book.objects.all())

    if not all_books:
        return []

    def clean_description(description):
        description = str(description).strip() if description else ""
        description = ''.join(c for c in description if c.isalnum() or c.isspace())[:50]
        return description

    descriptions = [clean_description(book.description) for book in all_books]

    if not any(descriptions):
        return []

    vectors = []
    for description in descriptions:
        try:
            response = client.embeddings.create(
                model="embedding-passage",
                input=[description]
            ).data
            vectors.append(response[0].embedding)
        except Exception as e:
            print(f"[ERROR] 임베딩 API 실패 (description: {description}): {e}")
            import logging
            logging.exception("임베딩 API 실패")
            return []

    vectors = np.array(vectors)

    try:
        base_idx = all_books.index(base_book)
    except ValueError:
        print(f"[ERROR] base_book({base_book})이 all_books에 없음")
        return []

    sim_matrix = cosine_similarity(vectors)
    try:
        sim_scores = list(enumerate(sim_matrix[base_idx]))
    except IndexError as e:
        print(f"[ERROR] sim_matrix에서 base_idx({base_idx}) 접근 오류: {e}")
        return []

    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)

    recommended = []
    for idx, score in sim_scores:
        if all_books[idx] == base_book:
            continue
        recommended.append(all_books[idx])
        if len(recommended) >= top_n:
            break

    # ✅ 3. 계산된 추천 결과를 DB에 저장
    recommendation = BookRecommendation.objects.create(base_book=base_book)
    recommendation.recommended_books.set(recommended)
    recommendation.save()

    return recommended