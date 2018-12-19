from importlib import import_module

from django.conf import settings
from django.contrib import messages
from django.contrib.auth import logout as auth_logout
from django.shortcuts import redirect
from django.utils.deprecation import MiddlewareMixin
from .models import UserSession

# Session backends : db/cache ...
SessionStore = import_module(settings.SESSION_ENGINE).SessionStore

class KickMiddleware(MiddlewareMixin):
    def process_response(self, request, response):
    # 1. 기록 전에 유저의 다른 세션들을 제거(강제 로그아웃)하고
        is_user_logined_in = getattr(request.user, 'is_user_logined_in', False)
        if is_user_logined_in:
            for user_session in UserSession.objects.filter(user=request.user):
                session_key = user_session.session_key
                session = SessionStore(session_key) # 세션키로 해당 세션들을 가져오기
                #session.delete()
                session['kicked'] = True
                session.save() # 원래 session middleware에서 save()처리를 하나, 지금은 middleware를 쓰지 않기 때문에 직접 save() 함수 호출
                user_session.delete() # 유저 세션 기록 제거

            # 2. 유저 세션을 새롭게 기록
            session_key = request.session.session_key
            UserSession.objects.create(user=request.user, session_key=session_key)

        return response

class KickedMiddleware(MiddlewareMixin):
    def process_request(self, request):
        kicked = request.session.pop('kicked', None) # kicked값을 가져옴과 동시에 제거
        if kicked:
            messages.info(request, '동일 아이디로 다른 브라우저 웹사이트에서 로그인이 감지되어 강제 로그아웃되었습니다.')
            auth_logout(request)
            return redirect(settings.LOGIN_URL)
