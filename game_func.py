import sys

import pygame
from bullet import Bullet
from alien import Alien
from time import sleep

def check_keydown_events(event, ai_settings, stats, screen, ship, bullets):
	''' 响应按键 '''
	if event.key == pygame.K_RIGHT:
		ship.moving_right = True
	elif event.key == pygame.K_LEFT:
		ship.moving_left = True
	elif event.key == pygame.K_SPACE:
		fire_bullet(ai_settings, screen, ship, bullets)
	elif event.key == pygame.K_q:
		filename = 'High_score.txt'
		with open(filename, 'w') as f_obj:
			f_obj.write(str(stats.high_score))
		sys.exit()

def check_keyup_events(event, ship):
	''' 响应松开 '''
	if event.key == pygame.K_RIGHT:
		ship.moving_right = False
	elif event.key == pygame.K_LEFT:
		ship.moving_left = False
		
def check_events(ai_settings, screen, stats, sb, play_button, ship, aliens, bullets):
	''' 响应鼠标或键盘事件 '''
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			filename = 'High_score.txt'
			with open(filename, 'w') as f_obj:
				f_obj.write(str(stats.high_score))
			sys.exit()
		elif event.type == pygame.KEYDOWN:
			check_keydown_events(event, ai_settings, stats, screen, ship, bullets)
		elif event.type == pygame.KEYUP:
			check_keyup_events(event, ship)
		elif event.type == pygame.MOUSEBUTTONDOWN:
			mouse_x, mouse_y = pygame.mouse.get_pos()
			check_play_button(ai_settings, screen, stats, sb, play_button, ship, \
				aliens, bullets, mouse_x, mouse_y)
			
def check_play_button(ai_settings, screen, stats, sb, play_button, ship, \
	aliens, bullets, mouse_x, mouse_y):
	''' 玩家单击play按钮时开始新游戏 '''
	button_clicked = play_button.rect.collidepoint(mouse_x, mouse_y)
	if button_clicked and not stats.game_active:
		#重置游戏设置
		ai_settings.initialize_dynamic_settings()
		#隐藏光标
		pygame.mouse.set_visible(False)
		#重新统计游戏信息
		stats.reset_stats()
		stats.game_active = True
		
		#重置积分牌图像
		sb.prep_images()
		
		#清空外星人和子弹列表
		aliens.empty()
		bullets.empty()
		
		#创建一群新的外星人,并让飞船置于其中
		creat_fleet(ai_settings, screen, ship, aliens)
		ship.center_ship()
		
def check_high_score(stats, sb):
	''' 检查是否诞生了最高分 '''
	if stats.score > stats.high_score:
		stats.high_score = stats.score
		sb.prep_high_score()

def update_screen(ai_settings, screen, stats, sb, ship, aliens, bullets, play_button):
	screen.fill(ai_settings.bg_color)
	# 在飞船和外星人后面重绘子弹
	for bullet in bullets.sprites():  #bullets.sprites() return a list 
		bullet.draw_bullet()
	sb.show_score()
	ship.blitme()
	aliens.draw(screen)     #对编组调用draw会自动绘制每个元素，位置由元素的rect决定
		
	if not stats.game_active:
		#游戏处于非活动状态，显示play按钮
		play_button.draw_button()
		
	#让最近绘制的屏幕可见	
	pygame.display.flip()
	
def update_bullets(ai_settings, screen, stats, sb, ship, aliens, bullets):
	''' 更新子弹设置，并删除已消失的子弹 '''
	#更新位置
	bullets.update()
	
	#删除已经消失的子弹
	for bullet in bullets.copy():
		if bullet.rect.bottom <= 0:
			bullets.remove(bullet)
	#print(len(bullets))  核实一下已消失的子弹是否被删除
	
	check_bullet_alien_collisions(ai_settings, screen, stats, sb, ship, aliens, bullets)
	
def check_bullet_alien_collisions(ai_settings, screen, stats, sb, ship, aliens, bullets):
	collisions = pygame.sprite.groupcollide(bullets, aliens, True, True)
	#groupcollide()返回的字典中添加一个键值对，两个True表明删除发生碰撞的子弹和外星人
	#与外星人碰撞的子弹都是字典collisions中的一个键
	#检查是否击中了外星人
	#如果击中了，就删除相应的子弹和外星人
	if collisions:
		for aliens in collisions.values():			#一个子弹可能击中多个外星人
			stats.score += ai_settings.alien_points * len(aliens)
			#乘上击中的外星人数目计入分数
			sb.prep_score()			#将得分渲染成图像
		check_high_score(stats, sb)
	if len(aliens) == 0:
		start_new_level(ai_settings, screen, stats, sb, ship, aliens, bullets)
		
def start_new_level(ai_settings, screen, stats, sb, ship, aliens, bullets):
		#删除现有子弹并新建一批外星人
		bullets.empty()
		ai_settings.increase_speed() 	#游戏难度加大
		stats.level += 1 				#游戏等级提高
		sb.prep_level()
		creat_fleet(ai_settings, screen, ship, aliens)
	
def check_fleet_edges(ai_settings, aliens):
	''' 在外星人到达边缘时采取相应的措施 '''
	for alien in aliens.sprites():
		if alien.check_edges():
			change_fleet_direction(ai_settings, aliens)
			break 
			
def change_fleet_direction(ai_settings, aliens):
	''' 将整群外星人下移，并改变它们的方向 '''
	for alien in aliens.sprites():
		alien.rect.y += ai_settings.fleet_drop_speed
	ai_settings.fleet_direction *= -1
	
def ship_hit(ai_settings, stats, sb, screen, ship, aliens, bullets):
	''' 响应被外星人撞到的飞船 '''
	if stats.ships_left > 0:
		stats.ships_left -= 1
		
		#更新飞船剩余数
		sb.prep_ships()
		
		#清空外星人列表和子弹
		aliens.empty()
		bullets.empty()
		
		#创建一批新的外星人，并将飞船置于屏幕底端中央
		creat_fleet(ai_settings, screen, ship, aliens)
		ship.center_ship()
		
		#暂停
		sleep(0.5)
	else:
		stats.game_active = False
		filename = 'High_score.txt'
		with open(filename, 'w') as f_obj:
			f_obj.write(str(stats.high_score))
		pygame.mouse.set_visible(True)
	
def check_alien_bottom(ai_settings, stats, sb, screen, ship, aliens, bullets):
	''' 检测是否有外星人到达了屏幕底端 '''
	screen_rect = screen.get_rect()
	for alien in aliens.sprites():
		if alien.rect.bottom >= screen_rect.bottom:
			ship_hit(ai_settings, stats, sb, screen, ship, aliens, bullets)
			break
		

def update_aliens(ai_settings, stats, sb, screen, ship, aliens, bullets):
	''' 更新外星人群中外星人的位置 '''
	check_fleet_edges(ai_settings, aliens)
	check_alien_bottom(ai_settings, stats, sb, screen, ship, aliens, bullets)
	aliens.update()
	
	#检测外星人和飞船之间的碰撞
	if pygame.sprite.spritecollideany(ship, aliens):
		#print("Ship Hit!!!")
		ship_hit(ai_settings, stats, sb, screen, ship, aliens, bullets)
	
def fire_bullet(ai_settings, screen, ship, bullets):
	''' 如果没有达到极限就发射一颗子弹 '''
	#创建一颗子弹，并存入编组bullets中
	if len(bullets) < ai_settings.bullets_allowed: 		#屏幕上最多3颗子弹
		new_bullet = Bullet(ai_settings, screen, ship)
		bullets.add(new_bullet)

def get_number_rows(ai_settings, ship_height, alien_height):
	''' 计算屏幕可以容纳多少行 '''
	available_space_y = (ai_settings.screen_height - (3 * alien_height) - ship_height)
	number_rows = int(available_space_y / (2 * alien_height))
	return number_rows
	
def get_number_aliens_x(ai_settings, alien_width):
	''' 计算每行可容纳多少外星人 '''
	available_space_x = ai_settings.screen_width - 2 * alien_width
	number_aliens_x = int(available_space_x / (2 * alien_width))
	return number_aliens_x
	
def creat_alien(ai_settings, screen, aliens, alien_number, row_number):
	''' 创建一个外星人并加入行 '''
	alien = Alien(ai_settings, screen)
	alien_width = alien.rect.width
	alien_height = alien.rect.height
	alien.x = alien_width + 2 * alien_width * alien_number
	alien.rect.x = alien.x
	alien.rect.y = alien_height + 2 * alien_height * row_number
	aliens.add(alien)
	
def creat_fleet(ai_settings, screen, ship, aliens):
	''' 创建外星人群 '''
	alien = Alien(ai_settings, screen)
	number_aliens_x = get_number_aliens_x(ai_settings, alien.rect.width)
	number_rows = get_number_rows(ai_settings, ship.rect.height, alien.rect.height)
	
	#创建外星人群
	for row_number in range(number_rows):
		for alien_number in range(number_aliens_x):
			creat_alien(ai_settings, screen, aliens, alien_number, row_number)
		
	
	
		