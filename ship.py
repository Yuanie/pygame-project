import pygame
from pygame.sprite import Sprite

class Ship(Sprite):
	
	def __init__(self, ai_settings, screen):
		''' 初始化飞船并设置其初始位置 '''
		super(Ship, self).__init__()
		self.screen = screen
		self.ai_settings = ai_settings
		#加载飞船图像并获取外接矩形
		self.image = pygame.image.load('images/ship.bmp')
		self.rect = self.image.get_rect()
		self.screen_rect = screen.get_rect()
		
		#将每艘新飞船设置在底部中央
		self.rect.centerx = self.screen_rect.centerx  #飞船中心x的坐标
		self.rect.bottom = self.screen_rect.bottom
		
		#在飞船的属性center中存储小数
		self.center = float(self.rect.centerx)
		
		#移动标志
		self.moving_right = False
		self.moving_left = False 
		
	def update(self):
		''' 根据移动标志调整飞船的位置 '''
		if self.moving_right and self.rect.right < self.screen_rect.right:
			#rect的右边缘小于屏幕右边缘
			self.center += self.ai_settings.ship_speed_factor
		if self.moving_left and self.rect.left > 0:  
			#rect的左边缘大于0
			self.center -= self.ai_settings.ship_speed_factor
			
		#rect的centerx属性只能存储整数值，因此作上下程序的变动	
		#根据self.center更新rect对象
		self.rect.centerx = self.center #只存储self.center的整数部分
			
	def blitme(self):
		''' 指定位置绘制飞船 '''
		self.screen.blit(self.image, self.rect)
		
	def center_ship(self):
		self.center = self.screen_rect.centerx