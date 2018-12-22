import os

class CBrowser:
    def upDir(self,browser):
        newDir = self.__get_parent_directory__(browser.getDir())

        browser.setDir(newDir)

    def enterDir(self, browser, dirname):
        newDir = os.path.join(browser.getDir(),dirname)
        browser.setDir(newDir)

    def get_folder_image(self, folder):
        #print("getting folder image:", folder)
        folders_imgs = os.listdir(folder)

        for _im in folders_imgs:
            if not os.path.isdir(os.path.join(folder, _im)):
                return _im

        #print("no image found")
        return None

    def __get_parent_directory__(self, dirpath):
        return os.path.relpath(os.path.join(dirpath, ".."))

