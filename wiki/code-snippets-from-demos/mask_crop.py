
def subtract_mask_from_img(img, mask):
    # RGBA - A
    if img.shape[3] == 4:
        subtracted_alphas = torch.min(img[0][:, :, 3], mask[0])
        return torch.cat(
            (
                img[0][:, :, :3],
                subtracted_alphas.unsqueeze(2),
            ),
            dim=2,
        ).unsqueeze(0)
    # RGB - A
    else:
        return torch.cat((img[0][:, :, :3], mask[0].unsqueeze(2)), dim=2).unsqueeze(
            0
        )