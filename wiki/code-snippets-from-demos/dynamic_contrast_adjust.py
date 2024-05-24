import torch

r, g, b = image1.unbind(-1)

luminance_image = .3 * r + .7 * g + .06 * b
luminance_mean = torch.mean(luminance_image.unsqueeze(-1))

# Adjust Contrast dynamically
contrast_adjust = 1.8
new_image = (image1.data * contrast_adjust) + (1.0 - contrast_adjust) * luminance_mean
new_image = torch.clamp(new_image, 0.0, 1.0)


print(new_image.shape)
image2.to(new_image)

