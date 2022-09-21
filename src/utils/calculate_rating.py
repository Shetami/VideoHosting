from src.auth_app.models.review_models import Rating


def calculate_rating(pk):
    rating = Rating.objects.filter(serial=pk)
    rating_count = Rating.objects.filter(serial=pk).count()
    sum_rating = 0
    for i in rating:
        sum_rating += i.rate
    if sum_rating != 0 and sum_rating is not None:
        sum_rating = sum_rating / rating_count
        return sum_rating
    else:
        return 0.00
