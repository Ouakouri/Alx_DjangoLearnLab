# Create Operation

## Command
```python
from books.models import Book

book = Book(title="1984", author="George Orwell", published_year=1949)
book.save()