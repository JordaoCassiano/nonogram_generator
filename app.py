import streamlit as st
import numpy as np
from PIL import Image, ImageDraw
import random
import io

def create_restrictions(board):
    def calculate_restrictions(line):
        res = []
        count = 0
        for cell in line:
            if cell == 1:
                count += 1
            elif count > 0:
                res.append(count)
                count = 0
        if count > 0:
            res.append(count)
        return res if res else [0]

    rows = [calculate_restrictions(board[i, :]) for i in range(board.shape[0])]
    cols = [calculate_restrictions(board[:, j]) for j in range(board.shape[1])]
    return {"rows": rows, "cols": cols}

def save_image(board, restrictions, filename):
    rows, cols = board.shape
    cell_size = 30
    width = cols * cell_size + 100
    height = rows * cell_size + 100

    image = Image.new("RGB", (width, height), "white")
    draw = ImageDraw.Draw(image)

    for i in range(rows):
        for j in range(cols):
            x0, y0 = j * cell_size + 50, i * cell_size + 50
            x1, y1 = x0 + cell_size, y0 + cell_size
            color = "black" if board[i, j] == 1 else "white"
            draw.rectangle([x0, y0, x1, y1], fill=color, outline="black")

    for i, row_res in enumerate(restrictions["rows"]):
        draw.text((10, i * cell_size + 55), " ".join(map(str, row_res)), fill="black")

    for j, col_res in enumerate(restrictions["cols"]):
        for k, val in enumerate(col_res):
            draw.text((j * cell_size + 55, 10 + k * 10), str(val), fill="black")

    buffer = io.BytesIO()
    image.save(buffer, format="PNG")
    buffer.seek(0)
    return buffer

def render_grid(board):
    rows, cols = board.shape
    cell_size = 30
    canvas = Image.new("RGB", (cols * cell_size, rows * cell_size), "white")
    draw = ImageDraw.Draw(canvas)

    for i in range(rows):
        for j in range(cols):
            x0, y0 = j * cell_size, i * cell_size
            x1, y1 = x0 + cell_size, y0 + cell_size
            color = "black" if board[i, j] == 1 else "white"
            draw.rectangle([x0, y0, x1, y1], fill=color, outline="gray")

    return canvas

def grid_interaction(board):
    rows, cols = board.shape
    for i in range(rows):
        for j in range(cols):
            key = f"cell_{i}_{j}"
            if st.button(" ", key=key, args=(board, i, j), help="Clique para alterar"):
                board[i, j] = 1 - board[i, j]
