# -*- coding: UTF-8 -*-

import	os,	pygame
import time as mtime
from pygame import *
import os

class ImageViewer:
	def __init__(self):
		self.clock = pygame.time.Clock()
		self.thezoom = 200
		self.xpos = 0
		self.smooth_xpos = 0
		self.imdir = "images/"
				
		pygame.init()
		pygame.font.init()
		font_size = 20
		self.main_font = pygame.font.SysFont("Arial", font_size, bold=False, italic=False)
		
		pygame.init	()

		pygame.display.set_mode((800,	600))	
		
		self.screen = pygame.display.get_surface()
		self.scr_mid = self.screen.get_height()/2
		
		self.load_images(self.imdir)
		
		while 1:
			self.updateScreen()

	def math_module(self,_number):
		if _number < 0:
			return (_number * -1)
		return _number

	def get_parent_directory(self,dirpath):
		return os.path.join(dirpath, "..")

	def update_smooth_xpos(self):
		
		if self.smooth_xpos != self.xpos:
			spdiff = self.xpos - self.smooth_xpos
			self.smooth_xpos += int(float(spdiff) * (0.4))
			
			if self.smooth_xpos < self.xpos:
				self.smooth_xpos +=1
			else:
				self.smooth_xpos -=1
		
	def updateScreen(self):
		self.screen.fill((255,255,255))		

		for	event	in	pygame.event.get():
			if	event.type	==	pygame.QUIT:
				exit(0)
				
			if	event.type	==	pygame.MOUSEBUTTONUP:
				xinc = 200
				
				if event.button == 5:
					self.thezoom -=100
					self.xpos -= xinc
				if event.button == 4:
					self.thezoom +=100
					self.xpos += xinc
					
				if event.button == 3:
					print "up one dir"
					print "self.imdir:", self.imdir
					
					foo ,imname= os.path.split(self.imdir)
					foo ,imname= os.path.split(foo)
					
					old_imdir = self.imdir
					self.imdir = self.get_parent_directory(self.imdir) + "/"	
					
					print "self.imdir", self.imdir
					if self.imdir == old_imdir:
						return
						
					self.load_images(self.imdir)	
					
					centered_newx = 0
					print self.xpos
					last_imw = 0
					for im_range in range(1,len(self.surfaces_info)):
						_imname, _imw = self.surfaces_info[im_range]
						if _imname == imname:
							print imname +" "  + _imname
							
							#estou com a imagem no canto esquerdo
							#coloco ela no centro
							centered_newx += (self.screen.get_width()/2) - (_imw/2)
							break
						last_imw = _imw
						centered_newx -= _imw
						print _imname + " " + imname
					print centered_newx
					self.xpos = centered_newx
					self.smooth_xpos = centered_newx					
					#sobe 1 diretorio parent
					
				if event.button == 1: #botao esquerdo
					#calcule em que imagem cliquei
					#obtendo posição do mouse
					mx,my = pygame.mouse.get_pos()
					realx = mx - self.xpos + self.surfaces[0].get_width()
					
					#calculando em que imagem cliquei
					if realx > 0 and my > (self.scr_mid/2) and my < ((3*self.scr_mid)/2):
						in_x = 0
						in_x2 = 0
						for n in range(len(self.surfaces_info)):
							info,width = self.surfaces_info[n]						
							in_x2 = in_x + width
							
							if realx < in_x2 and realx > in_x:							
								if not info.__contains__("/.."):	
									xpos = 0
									smooth_xpos = 0
									self.imdir = self.imdir + info + "/"
									self.load_images(self.imdir)
								
								break
							
							in_x = in_x2	
		
		scr_width = self.screen.get_width()		
		self.update_smooth_xpos()
		
		#imagem de fundo
		sf_x1 = 0
		while True:
			img_init_x = sf_x1 #+ smooth_xpos#xpos
			if(img_init_x < scr_width):
				self.screen.blit(self.surfaces[0],(img_init_x,0))
				
				sf_x1 += self.surfaces[0].get_width()
			else:
				break	
		
		sf_x = 0
		for n in range(1,len(self.surfaces)):
			img_init_x = sf_x + self.smooth_xpos#xpos
			if(img_init_x < scr_width):
				self.screen.blit(self.surfaces[n],(img_init_x,self.scr_mid/2))
				self.screen.fill([0x15,0x15,0x15], rect=[img_init_x,self.scr_mid/2,4,(self.scr_mid)])
				
				info,width= self.surfaces_info[n]
				
				#============================================
				#rendering text			
				text_surface = self.main_font.render(info,False,[0xff,0xff,0xff],[0x00,0x00,0x00])
				txw = text_surface.get_width()
				txh = text_surface.get_height()
				self.screen.blit(text_surface,[img_init_x + (width/2) - (txw/2),self.scr_mid/2 - txh,txw,txh])
				#============================================
				
				sf_x += self.surfaces[n].get_width()
			else:
				break			
				
		pygame.display.update()	
		self.clock.tick(12)
		#mtime.sleep(0.1)	
		
	def do_load_image(self,impath,is_parent):
		_img = pygame.image.load(impath)
		
		if len(self.surfaces) == 0:
			_img_rsz = self.resize_img(_img,self.screen.get_height())
		else:
			_img_rsz = self.resize_img(_img,self.screen.get_height()/2)
		
		self.surfaces.append(_img_rsz)
		
		head,tail = os.path.split(impath)
		head,tail = os.path.split(head)
		
		if is_parent:
			self.surfaces_info.append((tail + "/..",_img_rsz.get_width()))
		else:
			self.surfaces_info.append((tail,_img_rsz.get_width()))
		
	def get_folder_image(self,folder):
		print "getting folder image:", folder
		folders_imgs = os.listdir(folder)
		
		for _im in folders_imgs:
			if not os.path.isdir(folder + "/" + _im):	
				return _im
				
		print "no image found"
		return None
		
	def load_images(self,imgdir):
		self.surfaces = []
		self.surfaces_info = []
		
		folders = os.listdir(imgdir)	
		
		#=================================
		#load parent image
		pfolder_img = self.get_folder_image(self.imdir)
		if pfolder_img != None:
			parent_path = self.imdir + pfolder_img
			self.do_load_image(parent_path,True)
		#=================================	
		
		for f in folders:
			if(os.path.isdir(imgdir + f)):				
				fimg = self.get_folder_image(os.path.join(imgdir, f))
				
				if fimg != None:
					impath = self.imdir + f + '/' + fimg
					self.do_load_image(impath,False)
				
	def resize_img(self,myimage,height):
		aspect_ratio = float(myimage.get_width()) / float(myimage.get_height())
		myimage = pygame.transform.smoothscale(myimage, (int(height * aspect_ratio), height))	
		return myimage

imgv = ImageViewer()
			
			