import os
from PIL import Image
import io

TARGET_DIR = 'server/uploads/shops'
MAX_SIZE = 800 * 1024  # 800KB

def compress_image(filepath):
    filename = os.path.basename(filepath)
    try:
        file_size = os.path.getsize(filepath)
        if file_size <= MAX_SIZE:
            # print(f"Skipping {filename}: {file_size/1024:.2f}KB <= 800KB")
            return False

        print(f"Processing {filename}: {file_size/1024:.2f}KB")
        
        with Image.open(filepath) as img:
            img_format = img.format
            if not img_format:
                img_format = 'JPEG' if filename.lower().endswith(('.jpg', '.jpeg')) else 'PNG'
            
            # Handle mode for JPEG
            if img_format == 'JPEG' and img.mode != 'RGB':
                img = img.convert('RGB')

            # Compression loop
            quality = 90
            scale = 1.0
            
            while True:
                output_buffer = io.BytesIO()
                
                if scale < 1.0:
                    new_size = (int(img.width * scale), int(img.height * scale))
                    resized_img = img.resize(new_size, Image.Resampling.LANCZOS)
                else:
                    resized_img = img

                # Save to buffer
                save_args = {'format': img_format, 'optimize': True}
                if img_format == 'JPEG':
                    save_args['quality'] = quality
                
                resized_img.save(output_buffer, **save_args)
                
                size = output_buffer.tell()
                
                if size <= MAX_SIZE:
                    # Write back to file
                    with open(filepath, 'wb') as f:
                        f.write(output_buffer.getvalue())
                    print(f"  -> Compressed to {size/1024:.2f}KB (Scale: {scale:.2f}, Quality: {quality if img_format == 'JPEG' else 'N/A'})")
                    return True
                
                # Adjust parameters for next iteration
                if img_format == 'JPEG':
                    if quality > 70:
                        quality -= 5
                    else:
                        scale -= 0.1 # Reduce size if quality is already low
                else:
                    # For PNG or others, resize
                    scale -= 0.1
                
                if scale < 0.1: # Safety break
                    print(f"  -> Warning: Could not compress {filename} below 800KB even with severe reduction. Saving best effort.")
                    with open(filepath, 'wb') as f:
                        f.write(output_buffer.getvalue())
                    return True

    except Exception as e:
        print(f"Error processing {filename}: {e}")
        return False

def main():
    if not os.path.exists(TARGET_DIR):
        print(f"Directory not found: {TARGET_DIR}")
        return

    count = 0
    total_files = 0
    files = [f for f in os.listdir(TARGET_DIR) if f.lower().endswith(('.jpg', '.jpeg', '.png'))]
    total_files = len(files)
    
    print(f"Found {total_files} images in {TARGET_DIR}. Checking for files > 800KB...")

    for filename in files:
        filepath = os.path.join(TARGET_DIR, filename)
        if compress_image(filepath):
            count += 1
    
    print(f"Finished. Compressed {count} images.")

if __name__ == '__main__':
    main()
