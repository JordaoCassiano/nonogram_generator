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

st.title("Nonograma Criador")
dimensions = st.text_input("Insira a dimensão do nonograma (N x M, separado por vírgula):")

if dimensions:
    try:
        rows, cols = map(int, dimensions.split(","))
        board = np.zeros((rows, cols), dtype=int)

        st.write("Clique nas células para preenchê-las:")
        for i in range(rows):
            cols = st.columns(cols)
            for j, col in enumerate(cols):
                if st.session_state.get(f"cell_{i}_{j}", False):
                    board[i, j] = 1
                if col.button("⬛", key=f"cell_{i}_{j}"):
                    st.session_state[f"cell_{i}_{j}"] = not st.session_state.get(f"cell_{i}_{j}", False)

        restrictions = create_restrictions(board)
        st.write("Restrição por linhas:", restrictions["rows"])
        st.write("Restrição por colunas:", restrictions["cols"])

        if st.button("Gerar imagens"):
            full_image = save_image(board, restrictions, "nonograma_resultado.png")
            filled_positions = list(zip(*np.where(board == 1)))
            random.shuffle(filled_positions)

            partial_board = np.zeros_like(board)
            for r, c in filled_positions[: len(filled_positions) // 5]:
                partial_board[r, c] = 1

            partial_image = save_image(partial_board, restrictions, "nonograma_parcial.png")
            st.download_button("Baixar imagem completa", full_image, "nonograma_resultado.png")
            st.download_button("Baixar imagem parcial", partial_image, "nonograma_parcial.png")

    except ValueError:
        st.error("Dimensões inválidas! Por favor, insira no formato N,M.")
