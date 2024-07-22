from django.db import models

class ImportedData(models.Model):
    column_name = models.CharField(max_length=255)
    column_type = models.CharField(max_length=50, choices=[
        ('TEXT', 'TEXT'),
        ('INTEGER', 'INTEGER'),
        ('REAL', 'REAL'),
        ('BOOLEAN', 'BOOLEAN'),
        ('DATE', 'DATE'),
        ('TIMESTAMP', 'TIMESTAMP'),
    ])
    column_required = models.BooleanField(default=False)
    
    def __str__(self):
        return self.column_name
