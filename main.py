import cv2 as cv
import numpy as np
import streamlit as st
from PIL import Image

st.title("Your Online Signature ✒️")
st.markdown("Use this tool to make your signature ready to use on any digital file, and change the color of it for some extra fun! 🌟")

uploaded_file = st.file_uploader("Choose a signature image to upload! 📷")

if uploaded_file is not None:
    st.image(uploaded_file, "Uploaded Image 🖥️")

    image = Image.open(uploaded_file)
    img = np.array(image)

    gray_img = cv.cvtColor(img, cv.COLOR_RGB2GRAY)

    _, bw_img = cv.threshold(gray_img, 150, 255, cv.THRESH_BINARY)

    alpha_channel = np.ones_like(bw_img) * 255      #alpha channel is like a special layer on top of your regular image that tells the computer how transparent (or see-through) each pixel is
    alpha_channel[bw_img == 255] = 0                #make white parts transparent

    tr_img = cv.merge([bw_img, bw_img, bw_img, alpha_channel])          #apply to img

    color = st.radio("Do you want to change your signature's color? 🌈", ["yes 👍", "no 👎"], 1)

    if color == "yes 👍":
        color_picker = st.color_picker("🤔 Pick a color for the ink:", "#000000")
        ink_color = tuple(int(color_picker.lstrip("#")[i:i + 2], 16) for i in (0, 2, 4))       #seperates string hex into rgb, and tuples (connects) them

        save_img = tr_img.copy()

        save_img[bw_img == 0, 0] = ink_color[0]  # red
        save_img[bw_img == 0, 1] = ink_color[1]  # green
        save_img[bw_img == 0, 2] = ink_color[2]  # blue
    else:
        save_img = tr_img

    cv.imwrite("signaturez.png", save_img)
    st.image(save_img, "Processed Image 🖊️✨")

else:
    st.write("Please upload an image to start. 🖥️")