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
		return self.center
		
	
	def vida(self, dano):
		self._life -= dano
		return self._life
		

	def desenhar(self):
		if not self._enemy:
			pygame.draw.polygon(tela,self._cor,((self.midtop),(self.bottomleft),(self.bottomright)))
		else:
			pygame.draw.polygon(tela,self._cor,((self.midbottom),(self.topleft),(self.topright)))


class Projétil(Rect):
	def __init__(self, left, top, project_friend = True, project_especial = False):
		self.left = left
		self.top = top
		self.width = 6
		self.height = 100 if project_especial else 10
		self._vel = -15 if project_friend else 15
		self.dano = 100 if project_especial else 25


	def mover(self):
		self.top += self._vel
		

	def desenhar(self):
		pygame.draw.rect(tela, BRANCO,(self.left, self.top, self.width, self.height))
		self.mover()


def controle():
	return pygame.draw.polygon(tela,BRANCO, ((largura_tela//10*2, altura_tela//20*15), (largura_tela//10*8, altura_tela//20*15),(largura_tela//10*9, altura_tela//20*16),(largura_tela//10*8, altura_tela//20*17),(largura_tela//10*2, altura_tela//20*17),(largura_tela//10, altura_tela//20*16)))


todos_projetil = []
todos_inimigo = []

pygame.init()#INICIALIZA O MODULO
relogio = pygame.time.Clock()
fps = 60
vel = 10*(60//fps)
vel_i = vel*0.8

#Ajustes da tela
tela = pygame.display.set_mode()
largura_tela = tela.get_width()
altura_tela = tela.get_height()
print(f'Largura (X): {largura_tela}')
print(f'Altura (Y): {altura_tela}')
nj = Nave((largura_tela//2),(altura_tela//20*14))
ni = Nave((largura_tela//2),(altura_tela//20), enemy=True)

while True:
	relogio.tick(fps)
	tela.fill(PRETO)
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
				todos_projetil.append(Projétil(nj.midtop[0],nj.midtop[1]))
		if event.type == MOUSEBUTTONDOWN:
			if controle().collidepoint(event.pos):
				vel = -vel
				todos_projetil.append(Projétil(nj.midtop[0],nj.midtop[1]))
	
	for item in todos_projetil:
		if len(todos_projetil) > 0:
			item.desenhar()
			if item.colliderect((ni.left,ni.top, ni.width, ni.height)):
				todos_projetil.remove(item)
				if ni.vida(item.dano) <= 0:
					print('explodiu')
					ni = Nave((largura_tela//2)-50,(100), enemy=True)
					ni.vida(-100)
			elif item.top < 0:
				todos_projetil.remove(item)
	
	pygame.display.flip()
