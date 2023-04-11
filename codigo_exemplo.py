import escreve as le

img_entrada = 'img_in.jpeg'

img = le.criaImagemEditavel(img_entrada)
main_color = le.corDominante()
x, y = le.localizaLugarTexto(main_color)

texto = "Escrevendo na imagem aqui de boas. Bem de boas."
fonte = "arial.ttf"
tamanho = 55
cor = (240, 240, 240)

le.escreveImagem(img, x, y, texto, cor, fonte, tamanho)
 
