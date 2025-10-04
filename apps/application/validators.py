from django.core.exceptions import ValidationError

def validate_file_extension(value):
    import os
    ext = os.path.splitext(value.name)[1]  # fayl kengaytmasi
    valid_extensions = [".pdf", ".docx", ".jpg", ".png"]  # ruxsat berilgan formatlar
    if not ext.lower() in valid_extensions:
        raise ValidationError("Faqat pdf, docx, jpg, png fayllar yuklash mumkin.")

def validate_file_size(value):
    limit_mb = 50  
    if value.size > limit_mb * 1024 * 1024:
        raise ValidationError(f"Fayl hajmi {limit_mb} MB dan oshmasligi kerak.")
