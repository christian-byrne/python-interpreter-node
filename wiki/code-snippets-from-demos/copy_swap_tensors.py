print(f"image1 shape: {image1.shape}") 
print(f"image2 shape: {image2.shape}")

x = image1.copy()

image1.to(image2)
image2.to(x)

print(f"\nimage1 shape: {image1.shape}") 
print(f"image2 shape: {image2.shape}")

