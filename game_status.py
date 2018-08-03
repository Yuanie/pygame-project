class GameStats():
	''' 跟踪游戏的统计信息 '''
	
	def __init__(self, ai_settings):
		self.ai_settings = ai_settings
		self.reset_stats()
		self.game_active = False
		# 在任何情况下都不应重置最高得分
		self.high_score = 0
		
	def reset_stats(self):
		''' 初始化在游戏期间可能变化的统计信息 '''
		self.ships_left = self.ai_settings.ship_limit
		self.score = 0	#每次游戏开始就重置得分
		filename = 'High_score.txt'
		with open(filename, 'r') as f_obj:
			self.high_score = int(f_obj.read())
		self.level = 1
		
		