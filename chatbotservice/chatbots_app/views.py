from django.shortcuts import get_object_or_404
from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import ChatSession, ChatMessage
from .serializers import (
    ChatSessionSerializer,
    ChatMessageSerializer,
    NewMessageSerializer,
)

# /api/chat/sessions/
class ChatSessionListCreateView(generics.ListCreateAPIView):
    serializer_class = ChatSessionSerializer
    
    def get_queryset(self):
        queryset = ChatSession.objects.all()
        user_id = self.request.query_params.get('user_id')
        if user_id:
            queryset = queryset.filter(user_id=user_id)
        return queryset

# /api/chat/sessions/{session_id}/messages/
class MessageListCreateView(APIView):
    def get(self, request, session_id, *args, **kwargs):
        """
        Lấy danh sách tất cả tin nhắn trong một phiên chat.
        """
        session = get_object_or_404(ChatSession, id=session_id)
        messages = session.messages.all()
        serializer = ChatMessageSerializer(messages, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, session_id, *args, **kwargs):
        """
        Gửi một tin nhắn mới và nhận phản hồi từ bot.
        """
        session = get_object_or_404(ChatSession, id=session_id)
        serializer = NewMessageSerializer(data=request.data)
        
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        user_content = serializer.validated_data['content']
        
        # 1. Lưu tin nhắn của người dùng
        ChatMessage.objects.create(session=session, sender='USER', content=user_content)
        
        # 2. Tạo và lưu tin nhắn trả lời mẫu từ Bot
        # (Đây là nơi logic AI sẽ được tích hợp trong tương lai)
        bot_response_content = f"Cảm ơn bạn đã gửi tin nhắn. Tôi đã nhận được: '{user_content}'. Tôi là chatbot mẫu và sẽ sớm được nâng cấp."
        bot_message = ChatMessage.objects.create(session=session, sender='BOT', content=bot_response_content)
        
        # 3. Trả về phản hồi của bot
        response_serializer = ChatMessageSerializer(bot_message)
        return Response(response_serializer.data, status=status.HTTP_201_CREATED)