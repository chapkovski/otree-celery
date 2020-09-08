I tried to implement the app configuration in `o\celery.py`
but it fails to get access to the database.
For instance 
```python
from o.models import Player
print(Player.objects.all())
```

fails with:
```python
django.db.utils.OperationalError: no such table: o_player
```

apparently because the DB is not accessible by Celery.
