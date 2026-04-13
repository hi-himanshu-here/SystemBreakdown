import time
from django.http import JsonResponse

class RequestLoggingMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        start_time = time.time()

        print(f"➡️ Incoming request: {request.method} {request.path}")

        response = self.get_response(request)

        duration = time.time() - start_time
        print(f"Response: {response.status_code} in {duration:.4f}s")

        return response
    
class ErrorHandlingMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        try:
            response = self.get_response(request)
            return response
        except Exception as e:
            print(f"🔥 Error occurred: {str(e)}")

            from django.http import JsonResponse
            return JsonResponse({
                "error": "Something went wrong"
            }, status=500)
        
class RateLimitMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response
        self.requests = {}  # in-memory store

        self.LIMIT = 5
        self.WINDOW = 60  # seconds

    def __call__(self, request):
        ip = self.get_client_ip(request)
        current_time = time.time()

        if ip not in self.requests:
            self.requests[ip] = []

        # Remove old requests outside window
        self.requests[ip] = [
            timestamp for timestamp in self.requests[ip]
            if current_time - timestamp < self.WINDOW
        ]

        # Check limit
        if len(self.requests[ip]) >= self.LIMIT:
            return JsonResponse({
                "error": "Rate limit exceeded. Try again later."
            }, status=429)

        # Add current request
        self.requests[ip].append(current_time)

        return self.get_response(request)

    def get_client_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            return x_forwarded_for.split(',')[0]
        return request.META.get('REMOTE_ADDR')

class TokenBucketRateLimiter:

    def __init__(self, get_response):
        self.get_response = get_response
        self.capacity = 5          # max tokens
        self.refill_rate = 1       # tokens per second
        self.buckets = {}          # {ip: {tokens, last_refill}}

    def __call__(self, request):
        ip = self.get_client_ip(request)
        current_time = time.time()

        if ip not in self.buckets:
            self.buckets[ip] = {
                "tokens": self.capacity,
                "last_refill": current_time
            }

        bucket = self.buckets[ip]

        # Refill tokens
        elapsed = current_time - bucket["last_refill"]
        refill = elapsed * self.refill_rate

        bucket["tokens"] = min(self.capacity, bucket["tokens"] + refill)
        bucket["last_refill"] = current_time

        if bucket["tokens"] < 1:
            return JsonResponse({
                "error": "Rate limit exceeded (token bucket)"
            }, status=429)

        bucket["tokens"] -= 1

        return self.get_response(request)

    def get_client_ip(self, request):
        return request.META.get('REMOTE_ADDR')