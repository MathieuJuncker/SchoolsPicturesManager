import numpy as np
import os
import matplotlib.pyplot as  plt
from pathlib import Path
import pandas
import shutil
from skimage.measure import label, regionprops, regionprops_table
from PIL import Image
from PIL.ImageOps import invert

from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.properties import ObjectProperty, StringProperty
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.tabbedpanel import TabbedPanel
from kivy.uix.popup import Popup
from os.path import sep, expanduser, isdir, dirname
import sys

from kivy.lang import Builder

class MainWindow(Screen):
    pass

class FileChoosePopup(Popup):
    load = ObjectProperty()

class RenomerPhotosIndividuellesWindow(Screen):

    path_csv_file = StringProperty("Le chemin du fichier csv s'affihera ici")
    path_folder_depart = StringProperty("Le chemin du dossier de photos à renomer s'affihera ici")
    path_folder_arrive = None
    df_name_in_csv = None

    start_folder_ind_img = StringProperty('Tu dois selectionner un dossier de photos à renomer')
    file_path = StringProperty("No file chosen")
    the_popup = ObjectProperty(None)

    def open_popup(self):
        self.the_popup = FileChoosePopup(load=self.load)
        self.the_popup.open()

    def load(self, selection):
        self.path_csv_file = str(selection[0])
        self.the_popup.dismiss()
        print(self.path_csv_file)
        self.find_folder_depart()
        self.find_folder_arrive()
        self.read_csv_file()
    
    def find_folder_depart(self):
        s = self.path_csv_file.split('\\')
        self.path_folder_depart = '/'.join(s[:-1]) + '/Images a renomer/'
        if os.path.exists(self.path_folder_depart):
            print(os.listdir(self.path_folder_depart))
    
    def find_folder_arrive (self):
        s = self.path_csv_file.split('\\')
        self.path_folder_arrive = '/'.join(s[:-1]) + '/Images copie/'
        Path(self.path_folder_arrive).mkdir(exist_ok=True)

    
    def read_csv_file(self):
        df_name = pandas.read_csv(self.path_csv_file, encoding='latin1')
        df_name['namecomplet'] = df_name['Nom'] + ' ' + df_name['Prenom'].map(str) + ' ' + df_name['Classe']
        self.df_name_in_csv = df_name
        #for i in range (len(df_name['namecomplet'])):
        #    print(df_name['namecomplet'].loc[i])
    
    def rename_pictures(self):
        liste_fichiers_depart = os.listdir(self.path_folder_depart)
        for i in range (len(liste_fichiers_depart)):
            print(self.path_folder_depart + liste_fichiers_depart[i])
            print(self.path_folder_arrive + self.df_name_in_csv['namecomplet'].loc[i] + '.jpeg')
            shutil.copy(self.path_folder_depart + liste_fichiers_depart[i], self.path_folder_arrive + self.df_name_in_csv['namecomplet'].loc[i] + '.jpeg')



class PersonnaliserBDCWindow(Screen):

    path_img_bdc = StringProperty("Le chemin du BDC s'affihera ici")
    path_folder_bdc = None

    def open_popup(self):
        self.the_popup = FileChoosePopup(load=self.load)
        self.the_popup.open()

    def load(self, selection):
        self.path_img_bdc = str(selection[0])
        self.the_popup.dismiss()
        self.find_places_for_img()
        self.find_folder_arrive()

    def find_places_for_img (self):
        img = Image.open(self.path_img_bdc)
        back_up_img = img
        img = invert(img)
        img = img.convert('1')
        img_array = np.array(img)
        tree_blobs = label(img_array)
        properties =['area','bbox','convex_area','bbox_area',
             'major_axis_length', 'minor_axis_length',
             'eccentricity']
        df = pandas.DataFrame(regionprops_table(tree_blobs, properties = properties))
        print(df)
        for i in range (len(df)):
            copy_img = back_up_img
            width_img = df['bbox-3'].loc[i]-df['bbox-1'].loc[i]
            height_img = df['bbox-2'].loc[i]-df['bbox-0'].loc[i]
            copy_img = copy_img.resize((width_img,height_img))
            print(copy_img.size)
            back_up_img.paste(copy_img, (df['bbox-1'].loc[i],df['bbox-0'].loc[i]))
            back_up_img.save('C:/Users/junm/Desktop/img'+ str(i)+'.png')
            #print(df['area'].loc[i])

    def create_personal_bdc (self, df):
        img = Image.open(self.path_img_bdc)
        pass

    def find_folder_arrive (self):
        s = self.path_img_bdc.split('\\')
        self.path_folder_arrive = '/'.join(s[:-1]) + '/BDC/'
        Path(self.path_folder_arrive).mkdir(exist_ok=True)

    def create_BDC (self):
        pass

class GenererCommandesWindow(Screen):
    pass

class FaireTotalWindow(Screen):
    pass

class WindowManager(ScreenManager):
    pass

buildKV = Builder.load_file("schoolspicturesmanager.kv")

#SchoolsPicturesManagerApp --> remplacer par Gestionnaire_des_photos_de_classes --> penser à changer le nom
class Gestionnaire_des_photos_de_classes(App):
    def build(self):
        return buildKV

if __name__== "__main__":
    root = Gestionnaire_des_photos_de_classes()
    root.run()
