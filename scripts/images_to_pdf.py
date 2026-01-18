"""
Combine images into a PDF file for UIDAI submission.
Place all your page images in the 'submission_pages' folder and run this script.
Images will be sorted alphabetically/numerically and combined into a single PDF.
"""
from PIL import Image
import os
from pathlib import Path

def images_to_pdf(image_folder, output_pdf, dpi=300):
    """
    Combine all images in a folder into a single PDF.
    
    Args:
        image_folder: Path to folder containing images
        output_pdf: Output PDF filename
        dpi: Resolution for the PDF (default 300)
    """
    # Supported image formats
    image_extensions = {'.png', '.jpg', '.jpeg', '.bmp', '.tiff', '.webp'}
    
    # Get all image files and sort them
    image_folder = Path(image_folder)
    image_files = sorted([
        f for f in image_folder.iterdir() 
        if f.suffix.lower() in image_extensions
    ])
    
    if not image_files:
        print(f"No images found in {image_folder}")
        print(f"Supported formats: {', '.join(image_extensions)}")
        return False
    
    print(f"Found {len(image_files)} images:")
    for i, img in enumerate(image_files, 1):
        print(f"  {i}. {img.name}")
    
    # Load and convert images
    images = []
    for img_path in image_files:
        img = Image.open(img_path)
        # Convert to RGB if necessary (PDF doesn't support RGBA)
        if img.mode in ('RGBA', 'P'):
            # Create white background for transparent images
            background = Image.new('RGB', img.size, (255, 255, 255))
            if img.mode == 'P':
                img = img.convert('RGBA')
            background.paste(img, mask=img.split()[-1] if img.mode == 'RGBA' else None)
            img = background
        elif img.mode != 'RGB':
            img = img.convert('RGB')
        images.append(img)
    
    # Save as PDF
    if images:
        first_image = images[0]
        remaining_images = images[1:] if len(images) > 1 else []
        
        first_image.save(
            output_pdf,
            "PDF",
            resolution=dpi,
            save_all=True,
            append_images=remaining_images
        )
        
        print(f"\n✓ PDF created successfully: {output_pdf}")
        print(f"  Pages: {len(images)}")
        print(f"  Resolution: {dpi} DPI")
        return True
    
    return False

if __name__ == "__main__":
    # Configuration
    IMAGE_FOLDER = "submission_pages"  # Folder containing your page images
    OUTPUT_PDF = "UIDAI_1545_FINAL_SUBMISSION_IMAGES.pdf"
    
    # Create the folder if it doesn't exist
    os.makedirs(IMAGE_FOLDER, exist_ok=True)
    
    print("=" * 60)
    print("  PDF FROM IMAGES - UIDAI Submission Tool")
    print("=" * 60)
    print(f"\nLooking for images in: {os.path.abspath(IMAGE_FOLDER)}")
    print()
    
    if not any(Path(IMAGE_FOLDER).iterdir()):
        print(f"The '{IMAGE_FOLDER}' folder is empty!")
        print("\nInstructions:")
        print("1. Place your page images in the 'submission_pages' folder")
        print("2. Name them in order (e.g., page_01.png, page_02.png, ...)")
        print("3. Run this script again")
    else:
        images_to_pdf(IMAGE_FOLDER, OUTPUT_PDF)
