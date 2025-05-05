from django.contrib.sessions.middleware import SessionMiddleware


class SaveOldSessionKeyMiddleware(SessionMiddleware):

    def __call__(self, request):
        if request.session.session_key and not request.user.is_authenticated:
            if not request.session.has_key('old_session') or (request.session.has_key('old_session') and request.session['old_session'] != request.session.session_key):
                request.session['old_session_key'] = request.session.session_key
        return self.get_response(request)