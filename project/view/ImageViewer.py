# -*- coding: UTF-8 -*-

import os, pygame
import time as mtime
from pygame import *
import os
from model.domain.Browser import Browser
from controller.CBrowser import CBrowser


SURFACE_TYPE_FOLDER = 0
SURFACE_TYPE_IMAGE = 1

class SurfaceData:
    def __init__(self, surface, description, type, x, y):
        self.surface = surface
        self.description = description
        self.type = type
        self.x = x
        self.y = y


class ImageViewer:
    def __init__(self, basedir):
        self.X_INCREMENT = 200
        
        self.cursor_history = dict()

        self.background = None

        self.browser = Browser(basedir)
        self.cbrowser = CBrowser()
        self.clock = pygame.time.Clock()
        self.thezoom = 200
        self.xpos = 0
        self.smooth_xpos = 0
        pygame.init()
        pygame.font.init()
        font_size = 20
        self.main_font = pygame.font.SysFont("Arial", font_size, bold=False, italic=False)
        pygame.display.set_mode((800, 600))
        self.screen = pygame.display.get_surface()
        self.scr_mid = self.screen.get_height() / 2

        self.folderSurface = self.do_load_image("res/folder.png", int(float(self.screen.get_height()) / 1.3))

        self.load_images()

        while 1:
            self.updateScreen()

    def math_module(self, _number):
        if _number < 0:
            return (_number * -1)
        return _number

    def update_smooth_xpos(self):
        if self.smooth_xpos != self.xpos:
            prev_xpos = self.smooth_xpos

            spdiff = self.xpos - self.smooth_xpos
            self.smooth_xpos += int(float(spdiff) * (0.4))

            if self.smooth_xpos < self.xpos:
                self.smooth_xpos += 1
            else:
                self.smooth_xpos -= 1

            xpos_diff = self.smooth_xpos - prev_xpos

            for s in self.surfaces:
                s.x += xpos_diff

    def enterDir(self):
        # discovering which image was clicked
        mx, my = pygame.mouse.get_pos()

        for s in self.surfaces:
            if s.x > self.screen.get_width():
                break
            else:
                w = s.surface.get_width()
                h = s.surface.get_height()
                x = s.x
                y = s.y

                if mx > x and mx < x + w and my > y and my < y + h:
                    # saving current cursor
                    self.cursor_history.update({self.browser.getDir(): [self.xpos, self.smooth_xpos]})

                    self.cbrowser.enterDir(self.browser, s.description)
                    self.load_images()

                    #restoring cursor history
                    if self.browser.getDir() in self.cursor_history:
                        self.xpos, self.smooth_xpos = self.cursor_history[self.browser.getDir()]
                    else:
                        self.xpos = 0
                        self.smooth_xpos = 0

                    #update every new load surface x
                    print(self.xpos, self.smooth_xpos)
                    for sf in self.surfaces:
                        sf.x += self.xpos

                    break


    def upDir(self):
        # saving current cursor
        self.cursor_history.update({self.browser.getDir(): [self.xpos, self.smooth_xpos]})

        self.cbrowser.upDir(self.browser)
        self.load_images()

        # restoring cursor history
        if self.browser.getDir() in self.cursor_history:
            # last item on the stack
            self.xpos, self.smooth_xpos = self.cursor_history[self.browser.getDir()]
        else:
            self.xpos = 0
            self.smooth_xpos = 0

        for sf in self.surfaces:
            sf.x += self.xpos

    def updateSurfaces(self):

        scr_width = self.screen.get_width()
        self.update_smooth_xpos()

        #background image
        if self.background != None:
            sf_x1 = 0
            while True:
                img_init_x = sf_x1
                if (img_init_x < scr_width):
                    self.screen.blit(self.background, (img_init_x, 0))

                    sf_x1 += self.background.get_width()
                else:
                     break


        for actualSurface in self.surfaces:
            if actualSurface.type == SURFACE_TYPE_FOLDER:
                folder_x = actualSurface.x - (self.folderSurface.get_width()/2) + actualSurface.surface.get_width()/2
                self.screen.blit(self.folderSurface, (folder_x, self.scr_mid / 6))

            self.screen.blit(actualSurface.surface, (actualSurface.x  , actualSurface.y))


                # ============================================
                # rendering text
                #text_surface = self.main_font.render(info, False, [0xff, 0xff, 0xff], [0x00, 0x00, 0x00])
                #txw = text_surface.get_width()
                #txh = text_surface.get_height()
                #self.screen.blit(text_surface, [img_init_x + (width / 2) - (txw / 2), self.scr_mid / 2 - txh, txw, txh])
                # ============================================

                #if actualSurface.type == SURFACE_TYPE_FOLDER:
                #    sf_x += self.folderSurface.get_width()
                #else:
                #    pass#sf_x += self.surfaces[n].surface.get_width()
            #else:
            #    break

    def updateScreen(self):
        self.screen.fill((255, 255, 255))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit(0)

            if event.type == pygame.MOUSEBUTTONUP:
                #mouse whell anti-clockwise (scroll -)
                if event.button == 5:
                    #self.thezoom -= 100
                    self.xpos -= self.X_INCREMENT

                #mouse whell clockwise (scroll +)
                if event.button == 4:
                    #self.thezoom += 100
                    self.xpos += self.X_INCREMENT

                #up to parent directory and reload images
                if event.button == 3:
                    print(self.cursor_history)
                    self.upDir()
                    print(self.cursor_history)
                    print("===========")


                #enter directory
                if event.button == 1:  # botao esquerdo
                    print(self.cursor_history)
                    self.enterDir()
                    print(self.cursor_history)
                    print("============")

        self.updateSurfaces()

        pygame.display.update()
        self.clock.tick(12)

    def do_load_image(self, impath, resize_height):
        _img = pygame.image.load(impath)
        _img_rsz = self.resize_img(_img, resize_height)
        return _img_rsz

    def load_images(self):
        #TODO: TRY TO REMOVE DUPLICATE CODE IN THIS BLOCK
        print("loading images in:",self.browser.getDir())

        self.surfaces = []

        try:
            items = os.listdir(self.browser.getDir())
        except NotADirectoryError:
            self.cbrowser.upDir(self.browser)
            self.load_images()
            return

        x = 0
        for itm in items:
            #folders
            if os.path.isdir(os.path.join(self.browser.getDir(), itm)):
                fimg = self.cbrowser.get_folder_image(os.path.join(self.browser.getDir(), itm))

                if fimg != None:
                    impath = os.path.join(self.browser.getDir(), itm, fimg)
                    loadedImage = self.do_load_image(impath, self.screen.get_height() / 2)


                    x += (self.folderSurface.get_width()/2) - (loadedImage.get_width()/2)
                    surf = SurfaceData(loadedImage, itm, SURFACE_TYPE_FOLDER, x, self.scr_mid /2)
                    x += (loadedImage.get_width()/2) + (self.folderSurface.get_width()/2)
                    self.surfaces.append(surf)
                #empty folder
                else:
                    x += 0
                    surf = SurfaceData(self.folderSurface, itm, SURFACE_TYPE_FOLDER, x, self.scr_mid/2)
                    x += self.folderSurface.get_width()
                    self.surfaces.append(surf)


        #background image
        self.background = None

        #put images after folders
        for itm in items:
            if not os.path.isdir(os.path.join(self.browser.getDir(), itm)):
                impath = os.path.join(self.browser.getDir(), itm)
                loadedImage = self.do_load_image(impath, self.screen.get_height() / 2)

                x += (self.folderSurface.get_width() / 2) - (loadedImage.get_width() / 2)
                #x += self.folderSurface.get_width()
                surf = SurfaceData(loadedImage, itm, SURFACE_TYPE_IMAGE, x, self.scr_mid/2)
                x += (loadedImage.get_width() / 2) + (self.folderSurface.get_width() / 2)
                self.surfaces.append(surf)

                #loading background
                if self.background == None:
                    self.background = self.do_load_image(impath, self.screen.get_height())

    def resize_img(self, myimage, height):
        aspect_ratio = float(myimage.get_width()) / float(myimage.get_height())
        myimage = pygame.transform.smoothscale(myimage, (int(height * aspect_ratio), int(height)))
        return myimage



