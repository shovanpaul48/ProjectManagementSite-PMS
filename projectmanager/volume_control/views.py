# views.py

from django.shortcuts import render

def video_stream_view(request):
    return render(request, 'video_stream.html')