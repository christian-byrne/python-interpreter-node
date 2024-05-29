# Advanced Usage Tips

## Image/Tensor Types


- To understand the type and shape of the input images, please refer to the [Images, Latents, and Masks section of comfydocs.org](https://www.comfydocs.org/essentials/custom_node_images_and_masks).
- One thing not mentioned in those docs is that many (most) newer libraries expect tensors as **(B, C, H, W)**, while in Comfy they will be **(B, H, W, C)**. Those libraries/modules include `torchvision` and `fastai`.
- Additionally, be aware that the terms in the tensor are normalized to the range [0, 1] (torch.float32). 
- To get the color channels: `red, green, blue = image1.unbind(-1)`

### Alpha/Masks

- Alpha channels are automatically inverted when loaded in LoadImage nodes. To invert back to original: `mask1.to(1 - mask1)`
- You can retrieve the mask from the `mask` output link in the LoadImage node.
- If the original image did not have an alpha channel (it was in RGB format), the LoadImage node will still produce a mask of shaped (64, 64)

## Imports

You don't need to import `torch` to use the tensors class methods. But if you want to access torch methods directly, or any other libary/packet, you can import the module at the top of the code block. 

## Re-Assigning to New Types

In order to make all data from the inputs reference types with closures, all inputs are wrapped in a `Wrapper` class. There is an extended wrapper class for each builtin python type, as well as for `torch.Tensor` and `torch.nn.Module`.

The wrapper classes are designed the same way as the wrappers in the core `collections` module. Those wrappers were made so that programmers could extend primitive types as if they were classes. For example, the `collections.UserString` class allows you to your own add methods to strings while keeping all other behavior the same.

In general, the fact that the inputs/outputs are wrapped won't matter. The two caveats are listed in the [Usage](##usage) section of the README (re-assignment and passing variables as arguments to functions). 

An additional consideration is that while the `to()` method allows you to re-assign variables, if that re-assignment changes the type of the variable, you will lose access to many of that new variable's builtin methods. For example, if `number1` points to an integer originally, and you then re-assign that variable to point to a string, you will not be able to use `number1.split()` or `number1.replace()`. However, you can still use most operators and shared methods and of course you can still access the wrapped data and continue to re-assign it to other types.

This aspect probably won't change because the chance it causes an issue is low and when it does, it can easily be addressed by just using your own variables within the scope of the embedded code. Then to get the data out, assign to an output variable at the very end -- sort of treating the output variables as return statements. 
