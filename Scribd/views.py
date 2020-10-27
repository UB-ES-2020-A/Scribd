from django.shortcuts import render, redirect
from django.views.generic import CreateView, ListView, DetailView

from Scribd.models import Ebook
from Scribd.forms import EbookForm
from Scribd.serializers import ebookSerializer
from rest_framework import generics


# Create your views here.

def ebook_create_view(request):
    if request.method == 'POST':
        form = EbookForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('ebook_custom_list')
    else:
        form = EbookForm()
    return render(request, '../templates/forms/add_book.html', {'form': form})


class ebookListView(ListView):
    model = Ebook
    template_name = '../templates/scribd/ebooks_list.html'


class ebookDetailView(DetailView):
    model = Ebook
    template_name = '../templates/scribd/ebook_detail.html'


class ebookList(generics.ListCreateAPIView):
    queryset = Ebook.objects.all()
    serializer_class = ebookSerializer


class ebookDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Ebook.objects.all()
    serializer_class = ebookSerializer


def base(request):
    return render(request, '../templates/scribd/base.html')


def add_books_form(request):
    return render(request, '../templates/forms/add_book.html')
