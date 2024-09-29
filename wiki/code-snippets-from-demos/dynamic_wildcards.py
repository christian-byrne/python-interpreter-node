import random

# Assume you put the colors from the previous example into the text1 input for this node
complementary_color = text1

prompt = f"A {complementary_color} __wildcard_obj___ __wildcard_action__ in __wildcard_location__"

# Now take the text2 output and pipe to a wildcard node
text2.to(prompt)