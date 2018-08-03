#import sys  #先不用需要导入sys，因为只在game_func中使用了

import pygame
from pygame.sprite import Group

from settings import Settings
from ship import Ship
from game_status import GameStats
from button import Button
from score_board import ScoreBoard
#from alien import Alien
import game_func as gf

def run_game():
	#初始化游戏并创建一个屏幕对象
	pygame.init()
	ai_settings = Settings()
	screen = pygame.display.set_mode((ai_settings.screen_width, \
	ai_settings.screen_height)) 	#(850,600)是一个元组实参
	pygame.display.set_caption("Alien Invasion")
	#bg_color = (230, 230, 230)  
	
	play_button = Button(ai_settings, screen, "Play")
	
	#创建一个用于存储统计信息的实例,并创建积分牌
	stats = GameStats(ai_settings)
	sb = ScoreBoard(ai_settings, screen, stats)
	
	#创建飞船、一个用于存储子弹、外星人的编组
	ship = Ship(ai_settings, screen)
	bullets = Group()
	aliens = Group()
	
	#创建一个外星人群
	gf.creat_fleet(ai_settings, screen, ship, aliens)
	#游戏主循环
	while True:
		#监视键盘和鼠标事件
		gf.check_events(ai_settings, screen, stats, sb, play_button, ship, aliens, bullets)
		
		if stats.game_active:
			ship.update()
			gf.update_bullets(ai_settings, screen, stats, sb, ship, aliens, bullets)
			gf.update_aliens(ai_settings, stats, sb, screen, ship, aliens, bullets)
			
		#每次循环重绘屏幕
		gf.update_screen(ai_settings, screen, stats, sb, \
			ship, aliens, bullets, play_button)
	
		
run_game()

