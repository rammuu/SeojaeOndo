from openai import OpenAI
from sklearn.metrics.pairwise import cosine_similarity
from books.models import Book
import numpy as np
from django.conf import settings

# Upstage API 클라이언트 설정
client = OpenAI(
    api_key=settings.UPSTAGE_API_KEY,
    base_url="https://api.upstage.ai/v1/solar"
)

def recommend_books(base_title, top_n=3, base_book_id=None):
    base_book = Book.objects.filter(title__icontains=base_title).first()
    if not base_book:
        return []

    # base_book_id가 None이 아닌 경우, 해당 책과 동일한 카테고리의 책만 가져오기
    if base_book_id:
        try:
            base_book = Book.objects.get(pk=base_book_id)
            category = base_book.category
            all_books = list(Book.objects.filter(category=category))
        except Book.DoesNotExist:
            return []
    else:
        # 모든 책 가져오기
        all_books = list(Book.objects.all())

    if not all_books:
        return []

    book_ids = [book.id for book in all_books]

    def clean_description(description):
        description = str(description).strip() if description else ""
        description = ''.join(c for c in description if c.isalnum() or c.isspace())[:50]
        return description

    titles = [book.id for book in all_books]

    descriptions = [clean_description(book.description) for book in all_books]

    print("descriptions for embedding:", descriptions)

    if not any(descriptions):
        return []

    vectors = []
    for description in descriptions:
        try:
            response = client.embeddings.create(
                model="embedding-passage",
                input=[description]  # Pass each title individually
            ).data
            vectors.append(response[0].embedding)
        except Exception as e:
            print(f"[ERROR] 임베딩 API 실패 (description: {description}): {e}")
            import logging
            logging.exception("임베딩 API 실패")
            return []

    vectors = np.array(vectors)

    try:
        base_idx = next(i for i, id in enumerate(titles) if all_books[i].title == base_title)
    except StopIteration:
        print(f"[ERROR] base_title({base_title})을 titles에서 찾을 수 없습니다.")
        return []

    sim_matrix = cosine_similarity(vectors)
    try:
        sim_scores = list(enumerate(sim_matrix[base_idx]))
    except IndexError as e:
        print(f"[ERROR] sim_matrix에서 base_idx({base_idx})에 해당하는 값을 찾을 수 없습니다: {e}")
        return []

    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)

    recommended = []
    top_n = 6
    recommended = []
    for idx, score in sim_scores:
        if all_books[idx] == base_book:
            continue
        book = all_books[idx]
        recommended.append(book)
        if len(recommended) >= top_n:
            break

    return recommended
