from reader import app

app.config['SECRET_KEY'] = 'supersecretpassphrasehere'
SESSION_COOKIE_SECURE = True   
SESSION_COOKIE_HTTPONLY = True 
SESSION_COOKIE_SAMESITE = 'Lax'