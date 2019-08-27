import pygame
import random


#Assets_dir=path.join(path.dirname(__file__),"Assets")
#PNG_dir=path.join(Assets_dir,"PNG")

wWidth=900
wHeight=600
playZoneX=600
FPS=30
diem=0
miss=0



white=(255,255,255)
black=(0,0,0)
red=(255,0,0)
green=(0,255,0)
blue=(0,0,255)


def loadImg(name):
	a="Assets/PNG/"+name
	return pygame.image.load(a).convert_alpha()
def keyPressed(inputKey):
	key=pygame.key.get_pressed()
	if key[inputKey]:
		return True
	else:
		return False


#player and enemy spec
pWidth=50
pHeight=100
eWidth=16
eHeight=32

screen=pygame.display.set_mode((wWidth,wHeight))
pygame.display.set_caption("Hung bia :v")

#loading images
chay1=pygame.transform.scale(loadImg("chay1.png"),(pWidth,pHeight)).convert_alpha()
chay2=pygame.transform.scale(loadImg("chay2.png"),(pWidth,pHeight)).convert_alpha()
chay=[chay1,chay2]

bia=pygame.transform.scale(loadImg("bia.png"),(eWidth,eHeight)).convert_alpha()
tuongot=pygame.transform.scale(loadImg("tuongot.png"),(eWidth,eHeight)).convert_alpha()
dung=pygame.transform.scale(loadImg("dung.png"),(pWidth,pHeight)).convert_alpha()
background=loadImg("background.png")
hung=pygame.transform.scale(loadImg("hung.png"),(pWidth,pHeight)).convert_alpha()
chet=pygame.transform.scale(loadImg("chet.png"),(pHeight,pWidth)).convert_alpha()
anhgai1=pygame.transform.scale(loadImg("anhgaixinh1.png"),(wWidth-playZoneX,wHeight)).convert_alpha()
anhgai2=pygame.transform.scale(loadImg("anhgaixinh2.png"),(wWidth-playZoneX,wHeight)).convert_alpha()
anhgaixinh=[anhgai1,anhgai2]
drinks=[bia,tuongot]






clock=pygame.time.Clock()

all_sprites=pygame.sprite.Group()

class Animation:
	def __init__(self,sprite,speed):
		self.index=0
		self.sprite=sprite
		self.speed=speed
	def animate(self):
		Index=round(self.index)%len(self.sprite)
		self.index+=self.speed
		return int(Index)


class Player(pygame.sprite.Sprite):
    def __init__(self, width, height):
		pygame.sprite.Sprite.__init__(self)
		self.width=width
		self.height=height

		self.image=dung
		self.image.set_colorkey(black)
		self.rect=self.image.get_rect()
		self.rect.x=wWidth/2
		self.rect.bottom=wHeight

		self.animation=Animation(chay,0.5)
		self.hung=False
		self.chet=False
		self.speed=20
		self.mau=100

    def update(self):
		if  self.chet == False: 
			if keyPressed(pygame.K_UP):
				self.image=hung
				self.image.set_colorkey(black)
				self.hung=True
				self.mau-=2
				print self.mau

			elif keyPressed(pygame.K_LEFT) and self.rect.left>=1:
				self.rect.x-=self.speed
				index=self.animation.animate()
				self.image=chay[index]
				self.image.set_colorkey(black)
			elif keyPressed(pygame.K_RIGHT) and self.rect.right<=playZoneX-1:
				self.rect.x+=self.speed
				index=self.animation.animate()
				self.image=chay[index]
				self.image.set_colorkey(black)
			else:
				self.image=dung
				self.image.set_colorkey(black)
				self.hung=False
		else :
			self.image=chet
			self.image.set_colorkey(black)
			self.rect.bottom=650




class Enemy(pygame.sprite.Sprite):
    def __init__(self,width,height,player):
        pygame.sprite.Sprite.__init__(self)
        self.width=width
        self.height=height
        self.image=bia
        self.image.set_colorkey(black)
        self.player=player

        self.rect=self.image.get_rect()

        #self.rect.x=random.randint(1,wWidth)
        #self.rect.y=-wHeight
        self.rect.bottom=0
        self.rect.x=0
        #physics
        self.g=100
        self.time=0

    def update(self):
		self.rect.bottom+=self.g*0.5*self.time**2
		EbottomleftX= self.rect.x
		EbottomleftY =self.rect.bottom-self.width/2
		EbottomrightX= self.rect.x+self.width
		EbottomrightY =self.rect.bottom+self.width/2
		PtopleftX =self.player.rect.x
		PtopleftY= self.player.rect.y
		PtoprightX=self.player.rect.x+player.width
		PtoprightY=self.player.rect.y+player.height

		if EbottomleftX >=PtopleftX and EbottomrightX <= PtoprightX and EbottomleftY >= PtopleftY and EbottomrightY >=PtoprightY and self.player.hung and player.chet is not True and self.image is not tuongot:
			self.rect.bottom=0
			self.rect.x=random.randint(1,playZoneX)
			self.time=0
			global diem
			diem+=1
		elif (EbottomleftX >=PtopleftX and EbottomrightX <= PtoprightX and EbottomleftY >=PtopleftY and EbottomrightY >=PtoprightY):
			if player.hung is not True :
				player.chet= True
		elif self.rect.bottom>=wHeight:
			self.rect.bottom=0
			self.time=0
			self.rect.x=random.randint(1,playZoneX)
			if self.image==bia:
				global miss
				miss +=1
			print miss
			self.image=random.choice(drinks)

		elif (EbottomleftX >=PtopleftX and EbottomrightX <= PtoprightX and EbottomleftY >=PtopleftY and EbottomrightY >=PtoprightY):
			if player.hung is True and self.image==tuongot :
				player.chet = True
		if player.mau <=0:
			player.chet=True 

		self.time+=0.05
class HinhGai(pygame.sprite.Sprite):
	def __init__(self):
		pygame.sprite.Sprite.__init__(self)
		self.width=wWidth-playZoneX
		self.height=wHeight
		self.index=0
		self.image =anhgai1
		self.rect=self.image.get_rect()
		self.rect.x=playZoneX
	def update(self) :
		self.index=int(diem/2)
		self.image =anhgaixinh[self.index]

player=Player(pWidth,pHeight)
all_sprites.add(player)

enemy=Enemy(eWidth,eHeight,player)
all_sprites.add(enemy)
hinhgai=HinhGai()
all_sprites.add(hinhgai)
def gameLoop():
	running = True
	while running:
		clock.tick(FPS)
		for event in pygame.event.get():
		    if event.type== pygame.QUIT:
		        running= False

		screen.blit(background,background.get_rect())
		all_sprites.draw(screen)
		all_sprites.update()
		pygame.display.update()

gameLoop()
pygame.quit()
