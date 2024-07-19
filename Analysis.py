import sys
from PyQt5.QtWidgets import QApplication, QFileDialog,QComboBox, QWidget, QGridLayout, QPushButton,QLabel
from pathlib import Path
import matplotlib.ticker as ticker
from PyQt5.QtCore import Qt
import numpy as np
import pandas as pd
import seaborn as sns
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg, FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
from matplotlib.patches import Ellipse
import xlsxwriter


from matplotlib.pyplot import cm

from docs.layouts import Ui_analysWindow, Ui_S_a_Window, Ui_C_a_Window, Ui_D_a_Window

import os


class MainWindow(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.w = None
        self.w1 = None
        self.w2 = None  	
        
        self.ui = Ui_analysWindow()
        self.ui.setupUi(self)


        self.ui.clr.clicked.connect(self.gr_val)
        self.ui.sep.clicked.connect(self.sep_gr)
        self.ui.sel.clicked.connect(self.comp_c)
        self.ui.delt.clicked.connect(self.delt_f)
        self.ui.file_browse.clicked.connect(self.open_file_dialog)
        
        if not os.path.exists('temp'):
            os.mkdir('temp')
            
        if not os.path.exists('temp dist'):
            os.mkdir('temp dist')
        
        try:
            os.remove('temp/_temp2.pkl')
        except:
            print('no temp')
        
        self.show()
        
    def open_file_dialog(self):
        filename, _ = QFileDialog.getOpenFileName(
            self,
            "Select File",
            "C:/Users/10053684/Desktop/Play/Fragmented program",
            "Pickle file (*.pkl)"
        )
        if filename:
            self.ui.inp.addItems([str(Path(filename))])    
            
        X1 = pd.read_pickle(self.ui.inp.item(0).text())
        X1.to_pickle("temp/_temp2.pkl")
        
        
    def delt_f(self):
        self.ui.inp.clear() 
        
    def gr_val(self):
        self.w = ColorWindow()
        self.w.show()
            
            
    def sep_gr(self):
        self.w1 = SepWindow()
        self.w1.show()
        
    def comp_c(self):
        self.w2 = CompareWindow()
        self.w2.show()        

class ColorWindow(QWidget):

    def __init__(self):
        super().__init__()
        layout = QGridLayout()

        self.setLayout(layout)
        
        Xn = pd.read_pickle("temp/_temp2.pkl")
        itm = Xn.columns

        
        self.cb_platform = QComboBox(self)
        for i in itm:
            self.cb_platform.addItem(i)

        
        layout.addWidget(QLabel('Select parameter:'), 0, 0)
        layout.addWidget(self.cb_platform, 1, 0)
        
        self.cb_platform.activated.connect(self.draw)
        
        self.tr = Xn
        self.canvas = FigureCanvas(Figure(dpi = 150))
        layout.addWidget(self.canvas)
        
        self.save_button = QPushButton('Save')
        layout.addWidget(self.save_button)
        self.save_button.clicked.connect(self.save)
        
        
    def save(self):
         
        # selecting file path
        filePath, _ = QFileDialog.getSaveFileName(self, "Save Image", "",
                         "PNG(*.png);;JPEG(*.jpg *.jpeg);;All Files(*.*) ")
 
        # if file path is blank return back
        if filePath == "":
            return
         
        # saving canvas at desired path
        self.canvas.print_figure(filePath)
        
        
    def draw(self):
        
        Xn = self.tr
        col = self.cb_platform.currentText()
        y = np.ravel(Xn[col].values.tolist())

        self.canvas.figure.clf()
    
        with plt.style.context("ggplot"):
            
            tsne_result_df = pd.DataFrame({'tsne_1': Xn['tsne_1'].values.tolist(), 'tsne_2': Xn['tsne_2'].values.tolist(), 'label': y})
            ax = self.canvas.figure.subplots()
            sns.scatterplot(x='tsne_1', y='tsne_2', hue='label', data=tsne_result_df, ax=ax,s=5, palette = "icefire")
            ax.set_aspect('equal')
            ax.legend(bbox_to_anchor=(1.05, 1,), loc=2, borderaxespad=0.0,framealpha=0.99,markerscale=5)
            ax.xaxis.set_major_locator(ticker.NullLocator())
            ax.yaxis.set_major_locator(ticker.NullLocator())
            self.canvas.draw()
        
class SepWindow(QWidget):

    def __init__(self):
        super().__init__()

        self.s_ui = Ui_S_a_Window()
        self.s_ui.setupUi(self)
        
        Xn = pd.read_pickle("temp/_temp2.pkl")
        
        pop = Xn['id'].unique().tolist()

        
        for i in pop:
            self.s_ui.cb_platform.addItem(i)
            

        self.s_ui.adt.clicked.connect(self.adtt)
        self.s_ui.dl.clicked.connect(self.dll)
        self.s_ui.plt1.clicked.connect(self.dr1)
        self.s_ui.plt2.clicked.connect(self.dr2)
            
        
        self.s_ui.save_button.clicked.connect(self.save)
        self.s_ui.save_button2.clicked.connect(self.save2)
        
        
        for i in pop:
            self.s_ui.cb_platform2.addItem(i)
            
  
        self.s_ui.adt2.clicked.connect(self.adtt2)
        self.s_ui.dl2.clicked.connect(self.dll2)
            
        self.tr = Xn
        
        
    def save(self):
         
        # selecting file path
        filePath, _ = QFileDialog.getSaveFileName(self, "Save Image", "",
                         "PNG(*.png);;JPEG(*.jpg *.jpeg);;All Files(*.*) ")
 
        # if file path is blank return back
        if filePath == "":
            return
         
        # saving canvas at desired path
        self.s_ui.canvas1.print_figure(filePath)
        
        
    def save2(self):
         
        # selecting file path
        filePath, _ = QFileDialog.getSaveFileName(self, "Save Image", "",
                         "PNG(*.png);;JPEG(*.jpg *.jpeg);;All Files(*.*) ")
 
        # if file path is blank return back
        if filePath == "":
            return
         
        # saving canvas at desired path
        self.s_ui.canvas2.print_figure(filePath)
        
    def adtt(self):
        self.s_ui.gr_list.addItems([self.s_ui.cb_platform.currentText()])
    
    def dll(self):
        listItems=self.s_ui.gr_list.selectedItems()
        if not listItems: return        
        for item in listItems:
            self.s_ui.gr_list.takeItem(self.s_ui.gr_list.row(item))
            
    def adtt2(self):
        self.s_ui.gr_list2.addItems([self.s_ui.cb_platform2.currentText()])
    
    def dll2(self):
        listItems=self.s_ui.gr_list2.selectedItems()
        if not listItems: return        
        for item in listItems:
            self.s_ui.gr_list2.takeItem(self.s_ui.gr_list2.row(item))

        
    def dr1(self):
        
        Xn = self.tr
        pop = []
        for index in range(self.s_ui.gr_list.count()):
            pop.append(self.s_ui.gr_list.item(index).text())

        self.s_ui.canvas1.figure.clf()
        ax = self.s_ui.canvas1.figure.subplots(nrows=1, ncols=len(pop))
        
        
        
        j=0
        for i in pop:
            Xctr = Xn.loc[Xn['id'] == i]
            
            if len(pop)>1:
                if self.s_ui.rb_kde1.isChecked():
                    sns.kdeplot(x='tsne_1', y='tsne_2', data=Xctr, ax=ax[j],fill=True, thresh = 0.01, color = 'red')
                if self.s_ui.rb_scat1.isChecked():
                    sns.scatterplot(x='tsne_1', y='tsne_2', data=Xctr, ax=ax[j],s=5)
                ax[j].set_title(i)
                ax[j].set_aspect('equal')
                ax[j].xaxis.set_major_locator(ticker.NullLocator())
                ax[j].yaxis.set_major_locator(ticker.NullLocator())
                j+=1
            elif len(pop)==1: 
                if self.s_ui.rb_kde1.isChecked():
                    sns.kdeplot(x='tsne_1', y='tsne_2', data=Xctr, ax=ax,fill=True, thresh = 0.01, color = 'red')
                if self.s_ui.rb_scat1.isChecked():
                    sns.scatterplot(x='tsne_1', y='tsne_2', data=Xctr, ax=ax,s=5)
                ax.set_title(i)
                ax.set_aspect('equal')
                ax.xaxis.set_major_locator(ticker.NullLocator())
                ax.yaxis.set_major_locator(ticker.NullLocator())
            
        self.s_ui.canvas1.draw()
        
    def dr2(self):
        
        Xn = self.tr
        pop = []
        for index in range(self.s_ui.gr_list2.count()):
            pop.append(self.s_ui.gr_list2.item(index).text())
            
        self.s_ui.canvas2.figure.clf()
        ax = self.s_ui.canvas2.figure.subplots(nrows=1, ncols=len(pop))
        
        

        j=0
        for i in pop:
            Xctr = Xn.loc[Xn['id'] == i]
            
            if len(pop)>1:
                if self.s_ui.rb_kde2.isChecked():
                    sns.kdeplot(x='tsne_1', y='tsne_2', data=Xctr, ax=ax[j],fill=True, thresh = 0.01, color = 'red')
                if self.s_ui.rb_scat2.isChecked():
                    sns.scatterplot(x='tsne_1', y='tsne_2', data=Xctr, ax=ax[j],s=5)
                ax[j].set_title(i)
                ax[j].set_aspect('equal')
                ax[j].xaxis.set_major_locator(ticker.NullLocator())
                ax[j].yaxis.set_major_locator(ticker.NullLocator())
            elif len(pop)==1: 
                if self.s_ui.rb_kde2.isChecked():
                    sns.kdeplot(x='tsne_1', y='tsne_2', data=Xctr, ax=ax,fill=True, thresh = 0.01, color = 'red')
                if self.s_ui.rb_scat2.isChecked():
                    sns.scatterplot(x='tsne_1', y='tsne_2', data=Xctr, ax=ax,s=5)
                ax.set_title(i)
                ax.set_aspect('equal')
                ax.xaxis.set_major_locator(ticker.NullLocator())
                ax.yaxis.set_major_locator(ticker.NullLocator())
                
            j+=1
            
        self.s_ui.canvas2.draw()

class CompareWindow(QWidget):

    def __init__(self):
        super().__init__()
            
        self.c_ui = Ui_C_a_Window()
        self.c_ui.setupUi(self)

        Xn = pd.read_pickle("temp/_temp2.pkl")
        
        pop = Xn['id'].unique().tolist()


        for i in pop:
            self.c_ui.cb_platform.addItem(i)
            
        self.c_ui.cb_platform.activated.connect(self.dr1)
        
        self.c_ui.slider_x.valueChanged.connect(self.el_x)
        self.c_ui.slider_y.valueChanged.connect(self.el_y)
        self.c_ui.slider_w.valueChanged.connect(self.el_w)
        self.c_ui.slider_h.valueChanged.connect(self.el_h)
        self.c_ui.slider_phi.valueChanged.connect(self.el_phi) 
        self.c_ui.save_but.clicked.connect(self.save)
        self.c_ui.dist_but.clicked.connect(self.dist)
        self.c_ui.savefig_button.clicked.connect(self.savefig)       
        self.c_ui.savedat_button.clicked.connect(self.savedat) 
        
        self.tr = Xn
        
        self.plots = []
        self.names = []
        

        self.x_el = 50
        self.y_el = 50
        self.w_el = 50
        self.h_el = 50
        self.phi_el = 0

    def savefig(self):
         
        # selecting file path
        filePath, _ = QFileDialog.getSaveFileName(self, "Save Image", "",
                         "PNG(*.png);;JPEG(*.jpg *.jpeg);;All Files(*.*) ")
 
        # if file path is blank return back
        if filePath == "":
            return
         
        # saving canvas at desired path
        self.c_ui.canvas1.print_figure(filePath)

    def savedat(self):
         
        # selecting file path
        filePath, _ = QFileDialog.getSaveFileName(self, "Export data", "",
                         "xlsx(*.xlsx)")
 
        # if file path is blank return back
        if filePath == "":
            return
        
        workbook = xlsxwriter.Workbook(filePath)
        

        cl_nm = list(self.plots[0].columns)

        # saving plots at desired path
        
        for i in range(0,len(self.plots)):
            worksheet = workbook.add_worksheet(self.names[i])
            for j in range(0,len(cl_nm)):
                row = 1
                worksheet.write(0, j+1, cl_nm[j])
                l_pl = self.plots[i][cl_nm[j]].to_list()
                for item in l_pl:
                    worksheet.write(row, j+1, item)
                    row += 1
        
        workbook.close()

    def dr1(self):
        
        Xn = self.tr
        pop = self.c_ui.cb_platform.currentText()

        self.c_ui.canvas1.figure.clf()
        
        self.ax = self.c_ui.figure.subplots()
        
        Xctr = Xn.loc[Xn['id'] == pop]
        
        self.slg = Xctr
    
        if self.c_ui.rb_kde.isChecked():
            sns.kdeplot(x='tsne_1', y='tsne_2', data=Xctr, ax=self.ax,fill=True, thresh = 0.01, color = 'red')
        if self.c_ui.rb_scat.isChecked():
            sns.scatterplot(x='tsne_1', y='tsne_2', data=Xctr, ax=self.ax,s=5)
        
        
        self.ax.set_title(pop)
        self.ax.set_aspect('equal')
        self.ax.xaxis.set_major_locator(ticker.NullLocator())
        self.ax.yaxis.set_major_locator(ticker.NullLocator())

        self.xlms = self.ax.get_xlim()
        self.ylms = self.ax.get_ylim()
        
        self.x = self.xlms[0]+self.x_el*(self.xlms[1]-self.xlms[0])/100
        self.y = self.ylms[0]+self.y_el*(self.ylms[1]-self.ylms[0])/100
        self.h = self.h_el*(self.ylms[1]-self.ylms[0])/100/2
        self.w = self.w_el*(self.xlms[1]-self.xlms[0])/100/2

        self.ellipse = Ellipse(
        xy=(self.x, self.y),
        width=self.w,
        height=self.h,
        angle=0,
        facecolor="none",
        edgecolor="b"
        )

        self.ax.add_patch(self.ellipse)
        self.c_ui.canvas1.draw()
    
    def update(self):

        self.ellipse = Ellipse(
        xy=(self.x, self.y),
        width=self.w,
        height=self.h,
        angle=self.phi_el,
        facecolor="none",
        edgecolor="b"
        )
        
        
        self.ax.add_patch(self.ellipse)
        self.c_ui.canvas1.draw()

    def el_x(self, value):
        
        self.ellipse.remove()
        self.x_el = value
        self.x = self.xlms[0]+self.x_el*(self.xlms[1]-self.xlms[0])/100
        
        self.update()
        
    def el_y(self, value):
        
        self.ellipse.remove()
        self.y_el = value
        self.y = self.ylms[0]+self.y_el*(self.ylms[1]-self.ylms[0])/100
        
        self.update()
        
    def el_w(self, value):
        
        self.ellipse.remove()
        self.w_el = value
        self.w = self.w_el*(self.xlms[1]-self.xlms[0])/100/2
        
        self.update()

    def el_h(self, value):
        
        self.ellipse.remove()
        self.h_el = value
        self.h = self.h_el*(self.ylms[1]-self.ylms[0])/100/2

        self.update()
        
    def el_phi(self, value):
        
        self.ellipse.remove()
        self.phi_el = value
    
        self.update()
        
    def inellipse(self,x, y):
    
        theta = self.phi_el*np.pi/180
        xr = x - self.x
        yr = y-self.y
        x0 = np.cos(theta)*xr + np.sin(theta)*yr
        y0 = -np.sin(theta)*xr + np.cos(theta)*yr
        p = (pow(x0, 2)/pow(self.w, 2)) + (pow(y0, 2)/pow(self.h, 2))
    
        return p<1
        
    def save(self):
        
        Xn = self.tr
        pop = self.c_ui.cb_platform.currentText()
        Xctr = Xn.loc[Xn['id'] == pop]
        
        X1 = Xctr.copy()
        X1['p'] = list(map(self.inellipse, X1['tsne_1'], X1['tsne_2']))
        _plot = X1[X1['p'] == True]
        _out = self.c_ui.outp.text()
        
        self.plots.append(_plot)
        self.names.append(_out)
        
        self.w4 = SucWindow()
        self.w4.show()  
        
    def dist(self):
        
        for i in range(0,len(self.plots)):
            self.plots[i].to_pickle('temp dist/'+str(i)+'.pkl')
        
        df_n = pd.DataFrame(self.names, columns=['Names'])
        df_n.to_pickle('temp dist/Names.pkl')
            
        self.w3 = DistWindow()
        self.w3.show()  
        
class SucWindow(QWidget):
    def __init__(self):
        super().__init__()
        layout = QGridLayout()

        self.setLayout(layout)
        layout.addWidget(QLabel('Success!!!'), 0, 0)
        
class DistWindow(QWidget):

    
    def __init__(self):
        super().__init__()

        self.d_ui = Ui_D_a_Window()
        self.d_ui.setupUi(self)
        
        
        ct = len(os.listdir('temp dist'))
        
        self.plots=[]
        self.names = pd.read_pickle('temp dist/Names.pkl')['Names'].to_list()
    
        
        for i in range(0,ct-1):
            n = 'temp dist/'+str(i)+'.pkl'
            self.plots.append(pd.read_pickle(n))
            os.remove(n)
        
        os.remove('temp dist/Names.pkl')

            
            
        itm = self.plots[0].columns
        
        itm = itm[:-4]
        
        
        for i in itm:
            self.d_ui.cb_platform.addItem(i)
            self.d_ui.cb2_platform.addItem(i)
            self.d_ui.cb3_platform.addItem(i)
        
        self.d_ui.cb_platform.addItem("Number of events") 
        self.d_ui.cb_platform.addItem("Heatmap")     
           
        
        self.d_ui.cb_platform.activated.connect(self.draw)
        self.d_ui.cb2_platform.activated.connect(self.dotplot)
        self.d_ui.cb3_platform.activated.connect(self.dotplot)
        
        
        self.d_ui.savefig1_button.clicked.connect(self.savefig1)
        self.d_ui.savefig2_button.clicked.connect(self.savefig2)

        
        
    def savefig1(self):
         
        # selecting file path
        filePath, _ = QFileDialog.getSaveFileName(self, "Save Image", "",
                          "PNG(*.png);;JPEG(*.jpg *.jpeg);;All Files(*.*) ")
 
        # if file path is blank return back
        if filePath == "":
            return
         
        # saving canvas at desired path
        self.d_ui.canvas.print_figure(filePath)    


        
        
    def savefig2(self):
         
        # selecting file path
        filePath, _ = QFileDialog.getSaveFileName(self, "Save Image", "",
                          "PNG(*.png);;JPEG(*.jpg *.jpeg);;All Files(*.*) ")
 
        # if file path is blank return back
        if filePath == "":
            return
         
        # saving canvas at desired path
        self.d_ui.canvas2.print_figure(filePath)  
        
    def draw(self):
        col = self.d_ui.cb_platform.currentText()

        self.d_ui.canvas.figure.clf()
        
        self.d_ui.canvas.figure.set_tight_layout(True)
        
        
        ax = self.d_ui.canvas.figure.subplots()
        
        color = iter(cm.rainbow(np.linspace(0, 1, len(self.plots))))
        
        
        if col == "Number of events":
            ln, n_a = [],[]
            for i in range(0,len(self.plots)):
                ln.append(len(self.plots[i]))
                n_a.append(self.names[i])
            n_e = {'Area': n_a, '# events': ln}
            df_n_e = pd.DataFrame(n_e)
            sns.barplot(df_n_e, y="Area", x="# events", ax = ax, hue="Area", legend=False)
            
            
        elif col == "Heatmap":

            df_ls, n_a = [], []

            for i in range(0,len(self.plots)):
                n_a.append(self.names[i])
                _u = self.plots[i].copy() 
                _u = _u.drop('id', axis=1)
                _u = _u.drop('tsne_1', axis=1)
                _u = _u.drop('tsne_2', axis=1)
                _u = _u.drop('p', axis=1)
                df_ls.append(_u.median().to_frame())

            cnct = df_ls[0]
            for i in range(1,len(df_ls)):
                cnct = pd.concat([cnct, df_ls[i]], axis="columns")

            cnct.columns = n_a
            cnct = cnct.T

            sns.heatmap(cnct, cmap = 'hot', vmin = 0, vmax = 1, square=True, ax = ax, xticklabels=1, yticklabels=1).set(xlabel='', ylabel='')
            

        else:
            for i in range(0,len(self.plots)):
                c = next(color)
                sns.kdeplot(data=self.plots[i], x=col, ax = ax, label = self.names[i], linewidth = 2, c= c)
                ax.legend(bbox_to_anchor=(1.01, 1), borderaxespad=0)
        self.d_ui.canvas.draw()
        
    def dotplot(self):
        
        c1 = self.d_ui.cb2_platform.currentText()
        c2 = self.d_ui.cb3_platform.currentText()
        color = iter(cm.rainbow(np.linspace(0, 1, len(self.plots))))
        
        self.d_ui.canvas2.figure.clf()
        
        self.d_ui.canvas2.figure.set_tight_layout(True)
        
        ax = self.d_ui.canvas2.figure.subplots()
        
        for i in range(0,len(self.plots)):
            c = next(color)
            
            sns.scatterplot(x=c1, y=c2, data=self.plots[i], ax=ax,s=3, color=c,label = self.names[i])
            
        ax.legend(bbox_to_anchor=(1.01, 1), borderaxespad=0, markerscale=5)
        self.d_ui.canvas2.draw()
            

if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = MainWindow()
    sys.exit(app.exec())