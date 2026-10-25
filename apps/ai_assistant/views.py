import json
import uuid
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import ChatSession, ChatMessage
from .services import generate_ai_travel_response

@csrf_exempt
def chat_api(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'POST method required'}, status=405)

    try:
        data = json.loads(request.body.decode('utf-8'))
        user_message = data.get('message', '').strip()
        session_id = data.get('session_id')
    except Exception:
        return JsonResponse({'error': 'Invalid JSON body'}, status=400)

    if not user_message:
        return JsonResponse({'error': 'Empty message'}, status=400)

    # Resolve or create ChatSession
    user = request.user if request.user.is_authenticated else None
    if session_id:
        session = ChatSession.objects.filter(session_id=session_id).first()
    else:
        session = None

    if not session:
        session_id = str(uuid.uuid4())
        session = ChatSession.objects.create(session_id=session_id, user=user)
    elif user and not session.user:
        session.user = user
        session.save()

    # Save user message
    ChatMessage.objects.create(session=session, sender='user', content=user_message)

    # Generate smart AI reply
    bot_reply = generate_ai_travel_response(user, session, user_message)

    # Save bot response
    ChatMessage.objects.create(session=session, sender='assistant', content=bot_reply)

    return JsonResponse({
        'reply': bot_reply,
        'session_id': session.session_id,
        'timestamp': session.updated_at.strftime('%I:%M %p')
    })
