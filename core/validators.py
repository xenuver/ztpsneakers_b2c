from django.core.exceptions import ValidationError
import os

ALLOWED_IMAGE_EXTENSIONS = ['.jpg', '.jpeg', '.png', '.webp']
MAX_FILE_SIZE_MB = 5  # 5 MB

def validate_image_file(file):
    """Validator untuk file upload gambar."""
    if file is None:
        return
    
    # Validasi ekstensi
    ext = os.path.splitext(file.name)[1].lower()
    if ext not in ALLOWED_IMAGE_EXTENSIONS:
        raise ValidationError(
            f"Tipe file tidak didukung. Gunakan: {', '.join(ALLOWED_IMAGE_EXTENSIONS)}"
        )
    
    # Validasi ukuran file
    max_size_bytes = MAX_FILE_SIZE_MB * 1024 * 1024
    if file.size > max_size_bytes:
        raise ValidationError(
            f"Ukuran file terlalu besar. Maksimum {MAX_FILE_SIZE_MB}MB."
        )
    
    # Validasi magic bytes (MIME sniffing)
    # We must ensure we don't mess up file pointer
    file.seek(0)
    header = file.read(8)
    file.seek(0)
    
    MAGIC_BYTES = {
        b'\xff\xd8\xff': 'jpeg',
        b'\x89PNG\r\n\x1a\n': 'png',
        b'RIFF': 'webp',  # Simplified
    }
    
    is_valid = False
    for magic, fmt in MAGIC_BYTES.items():
        if header.startswith(magic):
            is_valid = True
            break
    
    if not is_valid:
        raise ValidationError("File yang diunggah bukan gambar yang valid.")
