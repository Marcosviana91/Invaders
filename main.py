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

	
	def vida(self, dano):
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


def coracao(top=0, left=0, tam=100):
	return pygame.draw.polygon(tela,ROSA_CHOQUE,((top+0,left+tam*0.25),(top+0,left+tam*0.5),(top+tam*0.5,left+tam),(top+tam,left+tam*0.5),(top+tam,left+tam*0.25),(top+tam*0.75,left),(top+tam*0.6,left),(top+tam*0.5,left+tam*0.25),(top+tam*0.4,left),(top+tam*0.25,left)))


def controle():
	return pygame.draw.polygon(tela,BRANCO, ((largura_tela//10*2, altura_tela//20*15), (largura_tela//10*8, altura_tela//20*15),(largura_tela//10*9, altura_tela//20*16),(largura_tela//10*8, altura_tela//20*17),(largura_tela//10*2, altura_tela//20*17),(largura_tela//10, altura_tela//20*16)))


todos_projetil = []
todos_inimigo = []

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
	
	msg_ponto = FONTE.render(f'Pontuação: {pontuação}', True, AZUL)
	msg_vida_jogador = FONTE.render(f'Vida da Nave do jogador: {nj.vida(0)}', True,VERDE)
	msg_vida_inimigo = FONTE.render(f'Vida da Nave do inimigo: {ni.vida(0)}', True, OURO)

	
	relogio.tick(fps)
	tela.fill(PRETO)
	tela.blit(msg_ponto,(0, 0))
	tela.blit(msg_vida_inimigo,(0, 80))
	tela.blit(msg_vida_jogador,(0, 160))
	controle()
	nj.desenhar()
	ni.desenhar()
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
	
	for projetil in todos_projetil:
		if len(todos_projetil) > 0:
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
					pygame.time.wait(2000)
			elif projetil.top < 0 or projetil.bottom > altura_tela:
				todos_projetil.remove(projetil)
	if pontuação > 0 and pontuação%4 == 0:
		print('desce coracao') #coracao((altura_tela/40)/fps))
	
	
	ni.top += ((altura_tela/20)/fps)
	contador += 1
	if contador == fps:
		contador = 0
		todos_projetil.append(ni.atirar())
	if ni.bottom > nj.top:
		break
	
	pygame.display.flip()
