import time


class RequestLogMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):

        start_time = time.time()

        response = self.get_response(request)

        end_time = time.time()

        duration = end_time - start_time

        if request.user.is_authenticated:
            username = request.user.username
        else:
            username = 'Anonymous'

        print(
            f"User: {username} | "
            f"Method: {request.method} | "
            f"Path: {request.path} | "
            f"Time: {duration:.2f} seconds"
        )

        return response