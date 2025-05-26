from openai import OpenAI
from sklearn.metrics.pairwise import cosine_similarity
from books.models import Book
import numpy as np
from django.conf import settings

# Upstage API 클라이언트 설정
client = OpenAI(
    api_key=settings.OPENAI_API_KEY,
    base_url="https://api.upstage.ai/v1/solar"
)

def recommend_books(base_title, top_n=3):
    try:
        base_book = Book.objects.get(title=base_title)
    except Book.DoesNotExist:
        return []

    # 모든 책 가져오기
    all_books = list(Book.objects.all())
    if not all_books:
        return []

    book_ids = [book.id for book in all_books]
    titles = [book.title for book in all_books]

    if not any(titles):
        return []

    try:
        response = client.embeddings.create(
            model="embedding-passage",  # Upstage 제목 임베딩 모델
            input=titles
        ).data
    except Exception as e:
        print(f"[ERROR] 임베딩 API 실패: {e}")
        return []

    vectors = np.array([r.embedding for r in response])

    try:
        base_idx = titles.index(base_title)
    except ValueError:
        return []

    sim_matrix = cosine_similarity(vectors)
    sim_scores = list(enumerate(sim_matrix[base_idx]))

    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)

    recommended = []
    for idx, score in sim_scores:
        if titles[idx] == base_title:
            continue
        recommended.append(all_books[idx])
        if len(recommended) >= top_n:
            break

    return recommended
