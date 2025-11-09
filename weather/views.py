from django.utils import timezone
from datetime import timedelta
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Weather
from .serializer import WeatherSerializer
from rest_framework.permissions import IsAuthenticated
import requests

class WeatherAPIView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        city = request.query_params.get('city')
        if not city:
            return Response(
                {'error': 'Please provide a city name using ?city=CityName'},
                status=status.HTTP_400_BAD_REQUEST
            )

        api_key = '6e5ed9e980477327a63a0e4ec4f7995c'   
        url = f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric'


        Weather.delete_old_data()


        recent_limit = timezone.now() - timedelta(minutes=5)
        existing = Weather.objects.filter(city__iexact=city, created_at__gte=recent_limit).first()
        if existing:
            serializer = WeatherSerializer(existing)
            return Response(serializer.data)


        try:
            response = requests.get(url, timeout=5)
            data = response.json()

            if response.status_code != 200:
                return Response(
                    {"message": data.get('message', 'Failed to fetch weather')},
                    status=response.status_code
                )

            weather_data = {
                'city': data['name'],
                'temperature': data['main']['temp'],
                'description': data['weather'][0]['description'],
                'humidity': data['main']['humidity'],
                'pressure': data['main']['pressure'],
            }


            obj = Weather.objects.create(**weather_data)
            serializer = WeatherSerializer(obj)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        except requests.exceptions.RequestException as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
