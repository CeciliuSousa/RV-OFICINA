import cv2
import numpy as np
import imageio

# Função para aplicar o efeito de distorção esférica
def aplicar_efeito_distorcao(frame):
    # Obter as dimensões do frame
    height, width = frame.shape[:2]
    
    # Gerar uma matriz de distorção
    f = 500
    cx, cy = width // 2, height // 2
    
    # Matriz de câmera
    camera_matrix = np.array([[f, 0, cx], [0, f, cy], [0, 0, 1]], dtype=np.float32)

    # Matriz de distorção
    dist_coeffs = np.array([0.2, 0.1, 0, 0], dtype=np.float32)

    # Aplicar a distorção esférica
    dst = cv2.undistort(frame, camera_matrix, dist_coeffs)
    return dst

# Função para gerar a visão estereoscópica (duas telas, uma para cada olho)
def gerar_visao_estereoscopica(frame, deslocamento_horizontal=30):
    # Desloca a imagem para a esquerda e para a direita para criar a visão estereoscópica
    imagem_esquerda = np.roll(frame, -deslocamento_horizontal, axis=1)
    imagem_direita = np.roll(frame, deslocamento_horizontal, axis=1)
    return imagem_esquerda, imagem_direita

# Caminho para o vídeo de entrada
video_input = 'video-exemplo-01.mp4'

# Usando ImageIO para garantir a leitura do vídeo corretamente
reader = imageio.get_reader(video_input)

# Verificar se o vídeo foi aberto corretamente
if reader.count_frames() == 0:
    print("Erro ao abrir o vídeo ou o arquivo está vazio!")
    exit()

# Obter as informações do vídeo
fps = reader.get_meta_data()['fps']
frame_width, frame_height = reader.get_meta_data()['size'] 

# Abrir a janela de vídeo com o tamanho final desejado
cv2.namedWindow("Visão VR", cv2.WINDOW_NORMAL)

# Loop para processar cada frame do vídeo
for i, frame in enumerate(reader):
    if frame is None:
        print("Erro ao ler o frame!")
        break
    
    # Redimensionar o frame
    frame_redimensionado = cv2.resize(frame, (640, 360))

    # Aplicar o efeito de distorção no frame redimensionado
    frame_com_efeito = aplicar_efeito_distorcao(frame_redimensionado)

    # Gerar a visão estereoscópica para VR
    frame_esquerda, frame_direita = gerar_visao_estereoscopica(frame_com_efeito)

    # Concatenar as imagens esquerda e direita para criar uma tela dividida
    tela_completa = np.hstack((frame_esquerda, frame_direita))

    # Exibir a tela dividida (visão VR)
    cv2.imshow('Visão VR', tela_completa)

    # Pressione 'q' para sair do vídeo
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Fechar a janela após terminar
cv2.destroyAllWindows()
