import pygame #install pip
from pygame.locals import *
from sys import exit
from cores import *
from random import choice


class Nave(Rect):
	def __init__(self, left, top, enemy= False, super= False):
		self.left = left
		self.top = top
		self.height = self.width = 500 if super else 100
		self._cor = VERMELHO if enemy else BRANCO
		self._enemy = enemy
		self._life = 500 if super else 100


	def mover(self, m_vel):
		self.left += m_vel
	
	
	def atirar(self):
		snd_shoot.play()
		return Projétil(self.midtop[0], self.midtop[1],self._enemy) if not self._enemy else Projétil(self.midbottom[0], self.midbottom[1],self._enemy)

	
	def vida(self, dano=0):
		if dano > 0:
			snd_hit.play()
		elif dano < 0:
			pass
		self._life -= dano
		return self._life
		

	def desenhar(self):
		if not self._enemy:
			pygame.draw.polygon(tela,self._cor,((self.midtop),(self.bottomleft),(self.bottomright)))
		else:
			pygame.draw.polygon(tela,self._cor,((self.midbottom),(self.topleft),(self.topright)))
		
	
	def Rect(self):
		return (self.left, self.top, self.width, self.height)


class Projétil(Rect):
	def __init__(self, left, top, project_enemy = False, project_especial = False):
		self.left = left
		self.top = top
		self.width = 6
		self.height = 100 if project_especial else 10
		self._vel = 15 if project_enemy else -15
		self.dano = 100 if project_especial else 25


	def mover(self):
		self.top += self._vel
		

	def desenhar(self):
		pygame.draw.rect(tela, BRANCO,(self.left, self.top, self.width, self.height))
		self.mover()


class Coracao(Rect):
	def __init__(self, left, top, tam):
		self.left = left
		self.top = top
		self.width = self.height = self.tam = tam


	def mover(self):
		self.top += 5
		

	def desenhar(self):
		pygame.draw.polygon(tela,ROSA_CHOQUE,((self.left+0,self.top+self.tam*0.25),(self.left+0,self.top+self.tam*0.5),(self.left+self.tam*0.5,self.top+self.tam),(self.left+self.tam,self.top+self.tam*0.5),(self.left+self.tam,self.top+self.tam*0.25),(self.left+self.tam*0.75,self.top),(self.left+self.tam*0.6,self.top),(self.left+self.tam*0.5,self.top+self.tam*0.25),(self.left+self.tam*0.4,self.top),(self.left+self.tam*0.25,self.top)))
		self.mover()


def controle():
	return pygame.draw.polygon(tela,BRANCO, ((largura_tela//10*2, altura_tela//20*15), (largura_tela//10*8, altura_tela//20*15),(largura_tela//10*9, altura_tela//20*16),(largura_tela//10*8, altura_tela//20*17),(largura_tela//10*2, altura_tela//20*17),(largura_tela//10, altura_tela//20*16)))


def fim_de_jogo():
	global pontuação
	global ni
	global nj
	global msg_ponto
	
	tela.fill(PRETO)
	fim = True
	msg_fim = FONTE.render('FIM DE JOGO', True, VERMELHO)
	msg_fim_rect = tela.blit(msg_fim,((largura_tela//2)-(msg_fim.get_width()//2), altura_tela//2))
	tela.blit(msg_ponto, ((largura_tela//2)-(msg_ponto.get_width()//2), (altura_tela//2) + msg_fim.get_height()))
	pygame.display.flip()
	while fim:
		for event in pygame.event.get():
			if event.type == QUIT:
				pygame.quit()
				exit()
			if event.type == KEYDOWN:
				if event.key == K_r:
					fim = False
			if event.type == MOUSEBUTTONDOWN:
				if msg_fim_rect.collidepoint(event.pos):
					fim = False
		todos_projetil.clear()
		pontuação = 0
		ni = Nave((largura_tela//2),(altura_tela//20), enemy=True)
		nj = Nave((largura_tela//2),(altura_tela//20*14))


todos_projetil = []
todos_inimigo = []
novo_coracao = None

fps = 60
contador = 0
pontuação = 0
vel = 10*(60//fps)
vel_i = vel*0.8


pygame.init()#INICIALIZA O MODULO
relogio = pygame.time.Clock()

#Ajustes da tela
tela = pygame.display.set_mode()
largura_tela = tela.get_width()
altura_tela = tela.get_height()
print(f'Largura (X): {largura_tela}')
print(f'Altura (Y): {altura_tela}')

#HUD
FONTE_PADRAO = pygame.font.get_default_font()
FONTE = pygame.font.SysFont(FONTE_PADRAO, largura_tela//10)
FONTEp = pygame.font.SysFont(FONTE_PADRAO, largura_tela//20)

###AUDIO### - https://themushroomkingdom.net/media/smw/wav
snd_shoot = pygame.mixer.Sound('sounds/shoot.wav') #smw_lava_bubble.wav
snd_hit = pygame.mixer.Sound('sounds/hit.wav') #smw_shell_ricochet.wav
snd_dies = pygame.mixer.Sound('sounds/nave_dies.wav') #smw_swooper_no_echo.wav

nj = Nave((largura_tela//2),(altura_tela//20*14))
ni = Nave((largura_tela//2),(altura_tela//20), enemy=True)

while True:
	msg_ponto = FONTEp.render(f'Score: {pontuação}', True, AZUL)
	msg_vida_jogador = FONTEp.render(f'Player Life: {nj.vida()}', True,VERDE)
	msg_vida_inimigo = FONTEp.render(f'Enemy Life: {ni.vida()}', True, OURO)
	msg_vida_em_inimigo = FONTEp.render(str(ni.vida()),True,VERMELHO)

	
	relogio.tick(fps)
	tela.fill(PRETO)
	l1 = tela.blit(msg_ponto,(0, 0))
	l2 = tela.blit(msg_vida_inimigo,(0, l1.bottom))
	tela.blit(msg_vida_jogador,(0, l2.bottom))
	controle()
	nj.desenhar()
	ni.desenhar()
	tela.blit(msg_vida_em_inimigo,(largura_tela//2, ni.top-FONTEp.get_height()))
	nj.mover(vel)
	ni.mover(vel_i)

	
	if nj.right == largura_tela:
		vel = -vel
	elif nj.right > largura_tela:
		nj.right = largura_tela-1
		vel = -vel
	elif nj.left == 0:
		vel = -vel
	elif nj.left < 0:
		nj.left = 1
		vel = -vel
	
	if ni.right == largura_tela:
		vel_i = -vel_i
	elif ni.right > largura_tela:
		ni.right = largura_tela-1
		vel_i = -vel_i
	elif ni.left == 0:
		vel_i = -vel_i
	elif ni.left < 0:
		ni.left = 1
		vel_i = -vel_i
		
	
	#eventos de interação (controles)
	for event in pygame.event.get():
		if event.type == QUIT:
			pygame.quit()
			exit()
		if event.type == KEYDOWN:
			if event.key == K_SPACE:
				vel = -vel
				todos_projetil.append(nj.atirar())
		if event.type == MOUSEBUTTONDOWN:
			if controle().collidepoint(event.pos):
				vel = -vel
				todos_projetil.append(nj.atirar())
	
	if len(todos_projetil) > 0:
		for projetil in todos_projetil:
			projetil.desenhar()
			if projetil.colliderect(ni.Rect()):
				todos_projetil.remove(projetil)
				if ni.vida(projetil.dano) <= 0:
					pontuação += 1
					snd_dies.play()
					ni = Nave((largura_tela//2)-largura_tela//20,(altura_tela//20), enemy=True)
					ni.vida(-pontuação*25)
			elif projetil.colliderect(nj.Rect()):
				todos_projetil.remove(projetil)
				if nj.vida(projetil.dano) <= 0:
					fim_de_jogo()
			elif projetil.top < 0 or projetil.bottom > altura_tela:
				todos_projetil.remove(projetil)
				
	if pontuação > 0 and pontuação%3 == 0 and novo_coracao is None:
		novo_coracao = Coracao(largura_tela//2,0,25)
	if novo_coracao is not None:
		novo_coracao.desenhar()
		if novo_coracao.colliderect(nj.Rect()):
			nj.vida(-novo_coracao.tam)
			novo_coracao = None
		elif novo_coracao.bottom > altura_tela:
			novo_coracao = None
		
	
	ni.top += ((altura_tela/20)/fps)
	contador += 1
	if contador == fps:
		contador = 0
		todos_projetil.append(ni.atirar())
	if ni.bottom > nj.top:
		fim_de_jogo()
	
	pygame.display.flip()
