from django.core.cache import cache


class RateLimitMiddleware:
    MAX_REQUESTS = 100
    WINDOW = 10

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        ip = request.META.get("REMOTE_ADDR")

        key = f"requests:{ip}"
        count = cache.get(key, 0) + 1
        cache.set(key, count, timeout=self.WINDOW)

        if count > self.MAX_REQUESTS:
            raise Exception("Too many requests.")

        return self.get_response(request)