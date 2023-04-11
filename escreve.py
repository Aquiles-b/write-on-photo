#-*- coding:utf-8 -*-
from PIL import Image, ImageFont, ImageDraw, ImageFilter
import numpy as np
import extcolors
import math
import os
import textwrap

#Cria as imagens de apoio e retorna a que será usada no final.
def criaImagemEditavel(input_name):
    img = Image.open(input_name)
    
    w, h = img.size
    prop = w / h 
    h_tmp = 500
    w_tmp = math.ceil(h_tmp*prop)
    h = 1000
    w = math.ceil(h*prop)

    img_tmp = img.resize((w_tmp, h_tmp))
    img_resized = img.resize((w, h))
    if(not os.path.exists('temp')):
        os.mkdir('temp')
    img_resized.save('temp/img_re.png')
    img_tmp.save('temp/img_tmp.png')

    return img_resized

#Retorna uma lista RGB com a cor dominante.
def corDominante():
    colors_x = extcolors.extract_from_path('temp/img_tmp.png', tolerance = 12, limit = 2)
    R = colors_x[0][0][0][0] 
    G = colors_x[0][0][0][1] 
    B = colors_x[0][0][0][2]

    main_color = [R,G,B]

    return main_color;

#Localiza a media dos pixels com a cor dominante e retorna coordenadas dele.
def localizaLugarTexto(main_color):
    img_re = Image.open('temp/img_re.png')
    im = np.array(img_re)
    Y, X = np.where(np.all( im==main_color,axis=2))

    x_final = sum(X)
    x_len = len(X) 
    y_final = sum(Y) 
    y_len = len(Y) 
    x_final = x_final// x_len
    y_final = y_final // y_len

    return x_final, y_final

#Escreve na imagem e salva.
def escreveImagem (img_re, x, y, texto, cor, fonte, tam):
    fontt = ImageFont.truetype(fonte, tam)
    x, y, linhas, anchor, espaco = melhorPosicao(x, y, texto, fontt, img_re)

    img_blur = img_re.filter(ImageFilter.GaussianBlur(3))

    img_ed = ImageDraw.Draw(img_blur)
    for line in linhas:
        img_ed.text((x, y), line, fill=cor, font=fontt, anchor=anchor, stroke_width=2, stroke_fill=(0,0,0))
        y += espaco

    img_blur.save('img_final.png')

#Com base nas coordenadas devolve uma localização padrão,
#limite de linhas e a justificação do texto. (x, y, texto com quebras, alinhamento, espaco)
def melhorPosicao(x, y, texto, fonte, img):
    espaco = fonte.getsize('hg')[1]
    w = fonte.getsize('m')[0]
    wid, h = img.size
    lim_x = wid//3
    lim_y = h//3
    empurrao = 30
    const = 30

    #Texto na esquerda.
    if (x< lim_x+const):
        print("Esq")
        anchor = "lt"
        if(y<lim_y):
            text = quebra_linha(texto, lim_x*1.7+const, w)
            return empurrao, empurrao, text, anchor, espaco
        elif (y<2*lim_y):
            text = quebra_linha(texto, lim_x*1.3+const, w)
            return empurrao, lim_y, text, anchor, espaco
        else:
            text = quebra_linha(texto, lim_x*1.7+const, w)
            return empurrao, lim_y*2, text, anchor, espaco
    #Texto centralizado
    elif (x< 2*lim_x-const):
        anchor = "mt"
        text = quebra_linha(texto, lim_x*2.4, w)
        if(y<lim_y):
            return lim_x*1.5, empurrao, text, anchor, espaco
        elif (y<2*lim_y):
            return lim_x*1.5, lim_y*1.5, text, anchor, espaco
        else:
            return lim_x*1.5, lim_y*1.5, text, anchor, espaco
    #Texto na direita.
    else:
        anchor = "rt"
        text = quebra_linha(texto, lim_x*1.7, w)
        if(y<lim_y):
            return 3*lim_x-empurrao, empurrao, text, anchor, espaco
        elif (y<2*lim_y):
            return 3*lim_x-empurrao, lim_y, text, anchor, espaco
        else:
            return 3*lim_x-empurrao, lim_y, text, anchor, espaco    

#Arruma o texto para escrever.
def quebra_linha(texto, largura, w):
    wid = math.ceil(largura/w) 
    lines = textwrap.wrap(texto, wid)

    return lines
