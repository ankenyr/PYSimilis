#Created by Robert Ankeny
#I assume no liability if this application harms your computer
#This application was built in my spare time as a learning project
#If you wish to borrow from my application or use it in your own please
#give credit. Thank you.
#Hashing algorithm was made from reading 
#http://www.hackerfactor.com/blog/index.php?/archives/432-Looks-Like-It.html
#Questions?? email: ankenyr@gmail.com
import wx
import os
import glob
import itertools
import ImageOps
import Image
from time import time
from scipy import fftpack

class ImageHash():
    hashnum = ''
    def __init__(self, file1):
        
        file1 = Image.open(file1)
        #Step one and two: Reduce Size and color
        file1 = file1.resize((32,32), Image.ANTIALIAS).convert('L')
        listOfInts = file1.getdata()
        listOfPixels = [float(integral) for integral in listOfInts]
        listOfPixels = fftpack.dct(listOfPixels)
        totalPixels = []
        counter = 0
        while counter < 8:
            totalPixels.extend(listOfPixels[counter*32:counter*32+8])
            counter+=1
        total = 0
        counter = 1
        while counter < len(totalPixels):
            average = total/len(totalPixels)
            counter+=1
        for pixel in totalPixels:
            if pixel < average:
                self.hashnum+='0'
            else:
                self.hashnum+='1'
                
class Imager(wx.App):
    img_width = 700
    img_height = 700
    img1 = ''
    img2 = ''
    img_array = []
    delete_list = []
    file_path = ''
    def __init__(self):
        wx.App.__init__(self, redirect=False)
        self.frame = wx.Frame(None,-1, title = 'Image')
        self.frame.SetSize(((self.img_width*2)+25,900))#Size of the frame
        self.panel = wx.Panel(self.frame)
        self.CreateMenuBar()
        self.CreatePictures()
        self.CreateButtons()
        self.CreateText()
        self.frame.Show()
        
    def OnClose(self, event):
        wx.Exit()
        
    def Choose1(self, event):
        self.RemoveImage(self.img1)
        self.delete_list.append(self.img1)
        self.ShowNewImage()
    
    def Choose2(self, event):
        self.RemoveImage(self.img2)
        self.delete_list.append(self.img2)
        self.ShowNewImage()
        
    def RemoveImage(self, imageToRemove):
        for i in self.img_array:
            if i[0] == imageToRemove:
                self.img_array.remove(i)
            elif i[1] == imageToRemove:
                self.img_array.remove(i)
        
    def Choose3(self, event):
        self.ShowNewImage()
     
    def CreateButtons(self):
        wx.Button(self.panel, 1, 'Delete me',(20,800),(200,30))
        self.Bind(wx.EVT_BUTTON, self.Choose1, id=1)
        wx.Button(self.panel, 2, 'Delete me',(1200,800),(200,30))
        self.Bind(wx.EVT_BUTTON, self.Choose2, id=2)
        wx.Button(self.panel, 3, 'Keep Both',(600,800),(200,30))
        self.Bind(wx.EVT_BUTTON, self.Choose3, id=3)
    
    def CreateMenuBar(self):
        menuBar = wx.MenuBar()
        fileMenu = wx.Menu()
        fileMenu.Append(100, "&Open Directory", "Opens a Directory")
        fileMenu.Append(101, "&Exit", "Exits Application")
        menuBar.Append(fileMenu, "&File")
        self.frame.SetMenuBar(menuBar)
        self.Bind(wx.EVT_MENU, self.OpenDir, id=100)
        self.Bind(wx.EVT_MENU, self.OnClose, id=101)
        self.Bind(wx.EVT_CLOSE, self.OnClose)
        
    def CreateText(self):
        self.file1_name = wx.TextCtrl(self.panel, -1, 'filename', 
          (0,self.img_height), style=wx.TE_READONLY)
        self.file1_resolution = wx.TextCtrl(self.panel, -1, 'resolution',
          (0,self.img_height+25), style=wx.TE_READONLY)
        self.file1_format = wx.TextCtrl(self.panel, -1, 'format',
          (0,self.img_height+50), style=wx.TE_READONLY)
        self.file1_size = wx.TextCtrl(self.panel, -1, 'size',
          (0,self.img_height+75), style=wx.TE_READONLY)

        self.file2_name = wx.TextCtrl(self.panel, -1, 'filename',
          (725,self.img_height), style=wx.TE_READONLY)
        self.file2_resolution = wx.TextCtrl(self.panel, -1, 'resolution',
          (725,self.img_height+25), style=wx.TE_READONLY)
        self.file2_format = wx.TextCtrl(self.panel, -1, 'format',
          (725,self.img_height+50), style=wx.TE_READONLY)
        self.file2_size = wx.TextCtrl(self.panel, -1, 'size',
          (725,self.img_height+75), style=wx.TE_READONLY)
        #self.file2_size.Clear()
        #self.file2_size.write('test')

    def CreatePictures(self):
        blankimg = wx.EmptyBitmap(self.img_width,self.img_height)
        self.imgDisplay1 = wx.StaticBitmap(self.panel, -1,blankimg,
          (0,0),(self.img_width,self.img_height))
        self.imgDisplay2 = wx.StaticBitmap(self.panel, -1,blankimg,
          (self.img_width+25,0),(self.img_width,self.img_height))
        
    def OpenImage(self, image):
        image = wx.Image(self.path+'\\'+image, wx.BITMAP_TYPE_ANY)
        image = image.Scale(self.img_width,self.img_height)
        return wx.BitmapFromImage(image)
    
    def OpenDir(self,event):
        dlg = wx.DirDialog(self.frame, "Select a directory of images")
        
        if dlg.ShowModal() == wx.ID_OK:
            self.path = dlg.GetPath()
        
        files = []
        for f in os.listdir(self.path):
            print f
            if os.path.splitext(f)[1].lower() in ('.jpg', '.jpeg',
                                                  '.bmp', '.png', '.gif'):
                files.append(f)
        progress = wx.ProgressDialog('Progress Bar',
          "Going through the folder"+self.path,
          maximum = len(list(itertools.combinations(files, 2))))
        count = 0
        timer = time()
        for file1, file2 in itertools.combinations(files, 2):
            progress.Update(count + 1, 'File 1: '+file1+'\nFile 2: '+file2)
            try:
                image1 = ImageHash(self.path+'\\'+file1)
                image2 = ImageHash(self.path+'\\'+file2)
            except:
                pass
            diffs=0
            for ch1, ch2 in zip(image1.hashnum,image2.hashnum):
                if ch1 != ch2:
                    diffs+=1
            #print file1+' '+file2
            #print diffs
            if diffs<=20:
                print 'found'
                self.img_array.append((file1, file2))
            if time() - timer > 10:
                wx.SafeYield()           
            count+=1
        progress.Destroy()
        self.ShowNewImage()

    def ShowNewImage(self):
        try:
            popper = self.img_array.pop()
            self.img1 = popper[0]
            self.img2 = popper[1]
            self.imgDisplay1.SetBitmap(self.OpenImage(popper[0]))
            self.imgDisplay2.SetBitmap(self.OpenImage(popper[1]))
            image1 = Image.open(self.path+'\\'+self.img1)
            self.file1_name.Clear()
            self.file1_name.write(self.img1)
            self.file1_resolution.Clear()
            self.file1_resolution.write('%s x %s'%image1.size)
            self.file1_format.Clear()
            self.file1_format.write('%s'%image1.format)
            self.file1_size.Clear()
            self.file1_size.write(str(os.path.getsize(self.path+'\\'+self.img1)))
            
            image2 = Image.open(self.path+'\\'+self.img2)
            self.file2_name.Clear()
            self.file2_name.write(self.img2)
            self.file2_resolution.Clear()
            self.file2_resolution.write('%s x %s'%image2.size)
            self.file2_format.Clear()
            self.file2_format.write('%s'%image2.format)
            self.file2_size.Clear()
            self.file2_size.write(str(os.path.getsize(self.path+'\\'+self.img2)))
        except IndexError:
            blankimg = wx.EmptyBitmap(self.img_width,self.img_height)
            self.imgDisplay1.SetBitmap(blankimg)
            self.imgDisplay2.SetBitmap(blankimg)
            self.file1_name.Clear()
            self.file2_name.Clear()
            self.file1_resolution.Clear()
            self.file2_resolution.Clear()
            self.file1_format.Clear()
            self.file2_format.Clear()
            self.file1_size.Clear()
            self.file2_size.Clear()
            self.DeleteFiles()
            self.img_array = []
            self.path = ''
            self.img1 = ''
            self.img2 = ''
            
            
    def DeleteFiles(self):
        for item in self.delete_list:
            try:
                os.remove(self.path+'\\'+item)
                print 'deleting file '+item
            except WindowsError:
                print 'No Files to delete'
        self.delete_list = []
        
if __name__ == '__main__':
    app = Imager()
    app.MainLoop()
    app.Destroy()