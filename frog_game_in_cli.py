import os;
import time;
import random;
import keyboard;
from typing import *;

SCREEN_WIDTH = 40;
SCREEN_HEIGH = 10;




EMPTY_CHAR = " ";


screen_matrix = [];
for i1 in range(SCREEN_HEIGH):
	row = [EMPTY_CHAR]*SCREEN_WIDTH;
	screen_matrix.append(row);


class CMD_COLOR:
	HEADER = '\033[95m'
	OKBLUE = '\033[94m'
	OKCYAN = '\033[96m'
	OKGREEN = '\033[92m'
	WARNING = '\033[93m'
	FAIL = '\033[91m'
	ENDC = '\033[0m'
	BOLD = '\033[1m';
	UNDERLINE = '\033[4m'


def make_text_red(text):
	return CMD_COLOR.FAIL+text+CMD_COLOR.ENDC;


def make_text_yellow(text):
	return CMD_COLOR.WARNING+text+CMD_COLOR.ENDC;

def make_text_green(text):
	return CMD_COLOR.OKGREEN+text+CMD_COLOR.ENDC;
	


class ScreenPixel:
	all_instance = [];
	def __init__(self, char,y,x):
		self.char = char;
		self.x = 0;
		self.y = 0;
		self.set_y_x(y, x);
		self.__class__.all_instance.append(self);


	def clear_from_matrix(self):
		global screen_matrix;
		screen_matrix[int(self.y)][int(self.x)] = EMPTY_CHAR;	


	def upadte_matrix(self):
		self.clear_from_matrix();
		screen_matrix[int(self.y)][int(self.x)] = self.char;



	def set_y_x(self,y,x):
		y %= SCREEN_HEIGH;
		x %= SCREEN_WIDTH;
		self.clear_from_matrix();
		global screen_matrix;
		self.x = x;
		self.y = y;
		self.upadte_matrix();


	def apply_y_x_diff(self, diff_y, diff_x):
		self.set_y_x(
			y=self.y+diff_y,
			x=self.x+diff_x,
			);
	


class ShortLastingPixel(ScreenPixel):
	all_instance = [];
	def __init__(self, char, x, y, frames_to_live:int):
		ScreenPixel.__init__(self, char, x, y)
		self.frames_to_live = frames_to_live;
		self.is_dead = False;

	def per_frame_function(self):
		if self.is_dead:
			return;
		if self.frames_to_live == 0:
			self.clear_from_matrix();
			self.is_dead = True;
		self.frames_to_live-=1;
		self.upadte_matrix();


	@classmethod
	def check_short_lasting_pixels(cls):
		for ins in cls.all_instance:
			ins.per_frame_function();



class Bullet(ScreenPixel):
	all_instance = [];
	def __init__(self, start_x, start_y, char, x_dif, y_dif, max_frames):
		ScreenPixel.__init__(self, char, start_y, start_x)
		self.x_dif = x_dif;
		self.y_dif = y_dif;
		self.max_frames = max_frames;
		self.age_by_frames_passd = 0;
		self.__class__.all_instance.append(self);

	def move(self):
		if self.age_by_frames_passd == self.max_frames:
			self.__class__.all_instance.remove(self);
			self.clear_from_matrix();
			return;

		if self.x == player.x and self.y == player.y:
			x_of_imapct = player.x;
			y_of_impact = player.y; 			
			bullet_life_time = 3;
			#BLOOD
			ScreenPixel(make_text_red("*"), x_of_imapct, y_of_impact);
			ScreenPixel(make_text_red("*"), x_of_imapct+1, y_of_impact);
			ScreenPixel(make_text_red("*"), x_of_imapct-1, y_of_impact);
			ScreenPixel(make_text_red("*"), x_of_imapct, y_of_impact-1);
			ScreenPixel(make_text_red("*"), x_of_imapct, y_of_impact+1);


		self.apply_y_x_diff(self.y_dif, self.x_dif)
		self.upadte_matrix();
		self.age_by_frames_passd += 1;


	@classmethod
	def update_all_bullets(cls):
		for i1 in cls.all_instance:
			i1.move();







def conditional_exec(func_to_call:Callable[[],None], cond:bool):
	def do_nothing():pass
	([do_nothing,func_to_call][int(cond)])();


def clear_screen():
	print(flush=True);
	os.system("cls");


def draw_screen():
	for row in screen_matrix:
		for pixel in row:
			print(pixel, end="");
		print("\n");



player:ScreenPixel = ScreenPixel(make_text_green("P"),2,2);


def move_player():
	global player;
	kp = keyboard.is_pressed;

	should_go_up=kp("w");
	should_go_down=kp("s");
	should_go_left=kp("a");
	should_go_right=kp("d");
	should_shoot=kp("e");

	def abstract_player_mover(var_name, diff_y, diff_x):
		def output():
			current_x = player.x;
			current_y = player.y;
			player.set_y_x(current_y+diff_y,current_x+diff_x,);
		return output;




	conditional_exec(abstract_player_mover("y",-1,0),should_go_up);
	conditional_exec(abstract_player_mover("y",+1,0),should_go_down);
	conditional_exec(abstract_player_mover("x",0,-1),should_go_left);
	conditional_exec(abstract_player_mover("x",0,+1),should_go_right);


traps_count = 0;
def make_random_traps():
	global traps_count;
	for i1 in range(random.choice([0,0,0,0,0,0,1,1,1,2])):
		Bullet(
		start_x=0,
		start_y=random.randint(3,SCREEN_HEIGH-2),
		char=make_text_red("C"),
		x_dif=0.5,
		y_dif=0,
		max_frames=SCREEN_WIDTH*2-1,
		);
		traps_count+=1;

frames_rendred = 0;
while True:
	make_random_traps();
	move_player();
	Bullet.update_all_bullets();	
	ShortLastingPixel.check_short_lasting_pixels();	
	draw_screen();
	if player.y == SCREEN_HEIGH-1:
		print(make_text_green("YOU WON!!!"));	
	time.sleep(0.05)
	clear_screen();
