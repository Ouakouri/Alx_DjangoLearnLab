# Create Operation

## Command
```python
from books.models import Book

book = Book.objects.create(title="1984", author="George Orwell", published_year=1949)