from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        # Добавляем пользовательские поля в токен
        token['email'] = user.email
        # У модели User нет username, поэтому добавим id или email как идентификатор
        token['user_id'] = user.id
        return token