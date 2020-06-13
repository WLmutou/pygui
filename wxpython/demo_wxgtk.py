#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function
# from tkinter import *
# from tkinter import filedialog
import wx

from PIL import Image  #, ImageTk

import os
import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
import torchvision.transforms as transforms
import torchvision.models as models
import copy

import time 
import base64

# import matplotlib as mpl
# mpl.use("TkAgg")
# import matplotlib.pyplot as plt



class PokerFrame(wx.Frame):
    def __init__(self, parent=None, id=-1, title="NEURAL STYLE"):
        wx.Frame.__init__(self, parent, id, title, size=(760,1050),
                          style=wx.DEFAULT_FRAME_STYLE ^ wx.RESIZE_BORDER)

        self.content_img_id = 10
        self.content_btn_id = 21
        self.style_img_id   = 112
        self.style_btn_id   = 123

        self.default_img_name = "images/none.png"

        self.content_img_name = self.default_img_name
        self.style_img_name   = self.default_img_name
        self.result_img_name  = self.default_img_name

        self.height = 200
        self.width = 380
        
        self.poker = wx.Panel(self, -1)
        self.panel = self.poker
        
        self.sizer = wx.GridBagSizer(10, 20 )  # 列间隔为10，行间隔为20
        ### 检查图片
        self.check_none_png()
        
        ### 创建界面 
        self.create_ui()
        

    def check_none_png(self):
        ### 需要一个空白图片，没有则创建
        if not os.path.exists(self.default_img_name):
            self.create_none_img()

            
    def create_none_img(self):
        if not os.path.exists("images"):
            os.mkdir("images")
        ### 图片data
        imgdata = base64.b64decode("iVBORw0KGgoAAAANSUhEUgAAAD0AAABRCAYAAABhVK7IAAAABHNCSV" +
                                   "QICAgIfAhkiAAAABl0RVh0U29mdHdhcmUAZ25vbWUtc2NyZWVuc2hv" +
                                   "dO8Dvz4AAAB1SURBVHic7c8xAQAgDMAwwL/nIWNHGgXtnZk5mLcdsK" +
                                   "FpRdOKphVNK5pWNK1oWtG0omlF04qmFU0rmlY0rWha0bSiaUXTiqYV" +
                                   "TSuaVjStaFrRtKJpRdOKphVNK5pWNK1oWtG0omlF04qmFU0rmlY0rW" +
                                   "haQU5/vBMEnqCtDtQAAAAASUVORK5CYII=")
        ### 写入图片
        with open(self.default_img_name, "wb") as f:
            f.write(imgdata)        
        

    def create_ui(self):
        self.Center()    # 窗口剧中
        size = (120, -1)
        
        ### 选择内容图片
        content_lbl = wx.StaticText(self.panel, label="请选择内容图片:")
        self.sizer.Add(content_lbl, pos=(0, 0), flag=wx.ALL, border=10)
        
        self.image1 = wx.Image( self.content_img_name, wx.BITMAP_TYPE_PNG).Rescale(self.width,self.height).ConvertToBitmap()
        self.bmp1 = wx.StaticBitmap(self.panel, self.content_img_id, self.image1)
        self.sizer.Add(self.bmp1, pos=(0,1), flag=wx.ALL, border=10)
        
        content_btn = wx.Button(self.poker, self.content_btn_id , label=u"浏览", size=size)
        content_btn.Bind(wx.EVT_BUTTON,self.OnOpenFile)   
        self.sizer.Add(content_btn, pos=(0, 2), span=(0, 3),flag=wx.ALL, border=10)


        ### 选择风格图片
        style_lbl = wx.StaticText(self.panel, label="请选择风格图片:")
        self.sizer.Add(style_lbl, pos=(1, 0), flag=wx.ALL, border=10)
        
        self.image2 = wx.Image( self.style_img_name, wx.BITMAP_TYPE_PNG).Rescale(self.width, self.height).ConvertToBitmap()
        self.bmp2 = wx.StaticBitmap(self.panel, self.style_img_id, self.image2)
        self.sizer.Add(self.bmp2, pos=(1,1), flag=wx.ALL, border=10)

        style_btn = wx.Button(self.panel, self.style_btn_id , label=u"浏览", size=size)
        style_btn.Bind(wx.EVT_BUTTON,self.OnOpenFile)                
        self.sizer.Add(style_btn, pos=(1, 2), span=(0, 3),flag=wx.ALL, border=10)
        
        #### 横线 ###
        line = wx.StaticLine(self.panel)
        self.sizer.Add(line, pos=(2, 0), span=(1, 8),
                  flag=wx.EXPAND|wx.BOTTOM, border=10)        

        ### 处理按钮
        exec_btn =  wx.Button(self.panel, 23 , label=u"处理", size=size)
        exec_btn.Bind(wx.EVT_BUTTON, self.onStart)
        self.sizer.Add(exec_btn, pos=(3, 1), span=(0, 1),flag=wx.ALL, border=10)
        
        quit_btn = wx.Button(self.panel, 24, label=u"退出", size=size)
        quit_btn.Bind(wx.EVT_BUTTON, self.onQuit)
        self.sizer.Add(quit_btn, pos=(3, 2), span=(0, 1),flag=wx.ALL, border=10)
                
        #### 横线 ###
        line = wx.StaticLine(self.panel)
        self.sizer.Add(line, pos=(4, 0), span=(1, 8),
                  flag=wx.EXPAND|wx.BOTTOM, border=10)
        
        #### 处理后的图片
        self.image3 = wx.Image(self.result_img_name, wx.BITMAP_TYPE_ANY).Rescale(720, 420).ConvertToBitmap()
        self.bmp3 = wx.StaticBitmap(self.panel, 12, self.image3)
        self.sizer.Add(self.bmp3, pos=(5,0),span=(1,8), flag=wx.ALL, border=10)   
        self.panel.SetSizerAndFit(self.sizer)
        
        
    def onChangeContentImg(self):
        image = wx.Image(self.content_img_name, wx.BITMAP_TYPE_ANY).Rescale(self.width, self.height).ConvertToBitmap()
        self.bmp1.SetBitmap(wx.Bitmap(image))

    def onChangeStyleImg(self):
        image = wx.Image(self.style_img_name, wx.BITMAP_TYPE_ANY).Rescale(self.width, self.height).ConvertToBitmap()
        self.bmp2.SetBitmap(wx.Bitmap(image))

    def onChangeResultImg(self):
        image = wx.Image(self.result_img_name, wx.BITMAP_TYPE_ANY).Rescale(720, 420).ConvertToBitmap()
        self.bmp3.SetBitmap(wx.Bitmap(image))

    def OnOpenFile(self,event):
        # wildcard = 'JPEG files (*.jpg)|*.jpg|PNG files (*.png)|*.png'
        wildcard = 'ALL files (*.*)|*.*'
        dialog = wx.FileDialog(None,u'select',os.getcwd(),'',wildcard,wx.DD_DEFAULT_STYLE)
        if dialog.ShowModal() == wx.ID_OK:
            sfname = dialog.GetPath()
            if not (sfname.endswith(".jpg") or sfname.endswith(".png") or sfname.endswith(".jpeg")):
                self.showMsg("请选择jpg或png文件")
                dialog.Destroy()
                return 
            if event.Id == self.style_btn_id:
                self.style_img_name = dialog.GetPath()
                self.onChangeStyleImg()
            elif event.Id == self.content_btn_id:
                self.content_img_name = dialog.GetPath()
                self.onChangeContentImg()
            dialog.Destroy()
            
    ## 消息提示
    def showMsg(self, msg):
        dlg = wx.MessageDialog(None, u"%s"%(msg), u"提醒", wx.ICON_QUESTION)
        if dlg.ShowModal() == wx.ID_YES:
            self.Close(True)
        dlg.Destroy()
        return
        
    ## 退出
    def onQuit(self,evt):
        wx.Exit()

    ## 启动处理
    def onStart(self, evt):
        print ("start...")        
        if self.content_img_name == self.default_img_name:
            self.showMsg("请先选择内容图片")
            return 
        if self.style_img_name == self.default_img_name:
            self.showMsg("请先选择风格图片")
            return 
        print ("goto start ...")
        try:
            self.result_img_name = neuralstyle(self.content_img_name, self.style_img_name)
            self.onChangeResultImg()
        except Exception as e:
            print (e)
            self.showMsg(e)



# 前端界面实现
def main():
    print ("main ...")
    app = wx.App(False)
    f = PokerFrame()
    f.Show()
    app.MainLoop()

    
def neuralstyle(contimg, stylimg):
    #设备为cpu
    device = torch.device("cpu")
    # 输出图片大小
    imsize = 128
    #输入图像的规模，调整其大小，并将其转化为torch张量
    #原始的PIL图片有在0-255之间的值，但是当转换成torch张量后，他们的值就转换成了0-1.为了有相同的维度，这些图片也需要被调整大小。一个重要的细节需要被注意——来自torch库的神经网络是使用值在0-1的张量来进行训练的。
    loader = transforms.Compose([
        transforms.Resize(imsize), 
        transforms.ToTensor()])
    #加载图像
    def image_loader(image_name):
        image = Image.open(image_name)
        image=image.resize((400,300))
        # fake batch dimension required to fit network's input dimensions 用来满足网络的输入维度的假batch维度，即不足之处补0
        image = loader(image).unsqueeze(0)
        return image.to(device, torch.float)
    #加载的风格图像和内容图像
    style_img = image_loader(stylimg)
    content_img = image_loader(contimg)
    #判断风格图像和内容图像是否大小一致，如果大小不一致则报错，说明需要大小一致的内容和风格图像
    assert style_img.size() == content_img.size(), \
        "we need to import style and content images of the same size"
    unloader = transforms.ToPILImage()
    def imshow(tensor,title=None):
        image = tensor.cpu().clone()  # we clone the tensor to not do changes on it
        image = image.squeeze(0)      # remove the fake batch dimension
        image = unloader(image)
        # image.save()
        # plt.imshow(image)
        # if title is not None:
        #    plt.title(title)
        # plt.pause(0.001) # pause a bit so that plots are updated        
    #损失函数的计算——内容损失函数
    class ContentLoss(nn.Module):
        def __init__(self, target,):
            super(ContentLoss, self).__init__()           
            self.target = target.detach()
        def forward(self, input):
            self.loss = F.mse_loss(input, self.target)
            return input
    def gram_matrix(input):
        a, b, c, d = input.size()  # a=batch size(=1)        
        features = input.view(a * b, c * d)  # resise F_XL into \hat F_XL
        G = torch.mm(features, features.t())  # compute the gram product
        return G.div(a * b * c * d)
    class StyleLoss(nn.Module):
        def __init__(self, target_feature):
            super(StyleLoss, self).__init__()
            self.target = gram_matrix(target_feature).detach()
        def forward(self, input):
            G = gram_matrix(input)
            self.loss = F.mse_loss(G, self.target)
            return input
    #导入模块，使用vgg19网络
    cnn = models.vgg19(pretrained=True).features.to(device).eval()
    cnn_normalization_mean = torch.tensor([0.485, 0.456, 0.406]).to(device)
    cnn_normalization_std = torch.tensor([0.229, 0.224, 0.225]).to(device)
    # create a module to normalize input image so we can easily put it in a
    # nn.Sequential
    class Normalization(nn.Module):
        def __init__(self, mean, std):
            super(Normalization, self).__init__()
            self.mean = torch.tensor(mean).view(-1, 1, 1)
            self.std = torch.tensor(std).view(-1, 1, 1)
        def forward(self, img):
            # normalize img
            return (img - self.mean) / self.std
    # desired depth layers to compute style/content losses :
    content_layers_default = ['conv_4']
    style_layers_default = ['conv_1', 'conv_2', 'conv_3', 'conv_4', 'conv_5']
    def get_style_model_and_losses(cnn, 
                                    normalization_mean, 
                                    normalization_std,
                                    style_img, 
                                    content_img,
                                    content_layers=content_layers_default,
                                    style_layers=style_layers_default):
        cnn = copy.deepcopy(cnn)
        # normalization module
        normalization = Normalization(normalization_mean, normalization_std).to(device)
        # just in order to have an iterable access to or list of content/syle
        # losses
        content_losses = []
        style_losses = []
        # assuming that cnn is a nn.Sequential, so we make a new nn.Sequential
        # to put in modules that are supposed to be activated sequentially
        model = nn.Sequential(normalization)
        i = 0  # increment every time we see a conv
        for layer in cnn.children():
            if isinstance(layer, nn.Conv2d):
                i += 1
                name = 'conv_{}'.format(i)
            elif isinstance(layer, nn.ReLU):
                name = 'relu_{}'.format(i)
                # The in-place version doesn't play very nicely with the ContentLoss
                # and StyleLoss we insert below. So we replace with out-of-place
                # ones here.
                layer = nn.ReLU(inplace=False)
            elif isinstance(layer, nn.MaxPool2d):
                name = 'pool_{}'.format(i)
            elif isinstance(layer, nn.BatchNorm2d):
                name = 'bn_{}'.format(i)
            else:
                raise RuntimeError('Unrecognized layer: {}'.format(layer.__class__.__name__))
            model.add_module(name, layer)
            if name in content_layers:
                # add content loss:
                target = model(content_img).detach()
                content_loss = ContentLoss(target)
                model.add_module("content_loss_{}".format(i), content_loss)
                content_losses.append(content_loss)
            if name in style_layers:
                # add style loss:
                target_feature = model(style_img).detach()
                style_loss = StyleLoss(target_feature)
                model.add_module("style_loss_{}".format(i), style_loss)
                style_losses.append(style_loss)
        # now we trim off the layers after the last content and style losses
        for i in range(len(model) - 1, -1, -1):
            if isinstance(model[i], ContentLoss) or isinstance(model[i], StyleLoss):
                break
        model = model[:(i + 1)]
        return model, style_losses, content_losses
    input_img = content_img.clone()
    def get_input_optimizer(input_img):
        # this line to show that input is a parameter that requires a gradient
        optimizer = optim.LBFGS([input_img.requires_grad_()])
        return optimizer
    def run_style_transfer(cnn, 
                            normalization_mean, 
                            normalization_std,
                            content_img, 
                            style_img, 
                            input_img, 
                            num_steps=300,
                            style_weight=100000, 
                            content_weight=1):
        """Run the style transfer."""
        print('Building the style transfer model..')
        model, style_losses, content_losses = get_style_model_and_losses(cnn,
                                                                        normalization_mean,
                                                                        normalization_std, 
                                                                        style_img, 
                                                                        content_img)
        optimizer = get_input_optimizer(input_img)

        print('Optimizing..')
        run = [0]
        while run[0] <= num_steps:
            def closure():
                # correct the values of updated input image
                input_img.data.clamp_(0, 1)
                optimizer.zero_grad()
                model(input_img)
                style_score = 0
                content_score = 0
                for sl in style_losses:
                    style_score += sl.loss
                for cl in content_losses:
                    content_score += cl.loss
                style_score *= style_weight
                content_score *= content_weight
                loss = style_score + content_score
                loss.backward()
                run[0] += 1
                if run[0] % 50 == 0:
                    print("run {}:".format(run))
                    print('Style Loss : {:4f} Content Loss: {:4f}'.format(
                        style_score.item(), 
                        content_score.item()))
                    print()
                return style_score + content_score
            optimizer.step(closure)
        # a last correction...
        input_img.data.clamp_(0, 1)
        return input_img
    output = run_style_transfer(cnn, 
                                cnn_normalization_mean, 
                                cnn_normalization_std,
                                content_img, 
                                style_img, 
                                input_img)
    # print ("output:", output)
    unloader = transforms.ToPILImage()
    image = output.cpu().clone()  # clone the tensor
    image = image.squeeze(0)  # remove the fake batch dimension
    image = unloader(image)
    result_img_name = os.path.join("images", str(time.time_ns()) + ".jpg")
    image.save(result_img_name)
    # plt.figure()
    #imshow(output,title="output image")
    # sphinx_gallery_thumbnail_number = 4
    # plt.ioff()
    # plt.show()
    print (result_img_name)
    return result_img_name
    
    
if __name__=="__main__":
    main()
