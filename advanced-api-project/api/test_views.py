from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from .models import Book, Author

class BookAPITestCase(APITestCase):
    
    def setUp(self):
        self.author = Author.objects.create(name="J.K. Rowling")
        self.book = Book.objects.create(title="Harry Potter", publication_year=1997, author=self.author)
        self.book_url = reverse('book-detail', kwargs={'pk': self.book.id}) 
        self.list_url = reverse('book-list') 

    def test_create_book(self):
        data = {"title": "New Book", "publication_year": 2022, "author": self.author.id}
        response = self.client.post(self.list_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Book.objects.count(), 2)
    
    def test_retrieve_book(self):
        response = self.client.get(self.book_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], self.book.title)
    
    def test_update_book(self):
        data = {"title": "Updated Title", "publication_year": 2000, "author": self.author.id}
        response = self.client.put(self.book_url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.book.refresh_from_db()
        self.assertEqual(self.book.title, "Updated Title")
    
    def test_delete_book(self):
        response = self.client.delete(self.book_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Book.objects.count(), 0)

