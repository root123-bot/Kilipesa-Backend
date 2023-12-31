from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import smart_str, force_str, smart_bytes, DjangoUnicodeDecodeError
# (smart_str, force_str, smart_bytes is used to make sure we're sending the convectional data the data that browser/gmail understand..)
from django.utils.http import urlsafe_base64_decode


class RegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ['email', 'password']  



class EmailSerializer(serializers.Serializer):
    email = serializers.EmailField()


    class Meta:
        fields = ('email',)



class ResetPasswordSerializer(serializers.Serializer):
    password = serializers.CharField(
        write_only=True,
        min_length=4
    )

    class Meta:
        fields = ('password')


    def validate(self, data):
        password = data.get("password")
        token = self.context.get("kwargs").get('token')   # remember in our view we passed kwargs containing token and encoded id in context keyword/variable
        encoded_pk = self.context.get("kwargs").get('encoded_pk')

        if token is None or encoded_pk is None:
            raise serializers.ValidationError('Some data missing here')

        pk = urlsafe_base64_decode(encoded_pk).decode()
        user = get_user_model().objects.filter(pk=pk).first() # i use filter to not get error like in .get() when user does not exist

        if user:
            if not PasswordResetTokenGenerator().check_token(user, token): 
                raise serializers.ValidationError('The token is invalid') 

            user.set_password(password)   
            user.save()

            return data
        
        else:
            return('error', 'the user is not existed maybe its deleted...')