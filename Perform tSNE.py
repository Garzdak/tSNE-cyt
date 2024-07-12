import sys
from PyQt5.QtWidgets import QApplication, QFileDialog, QWidget,QListWidgetItem,QAbstractItemView, QGridLayout, QLineEdit, QPushButton, QListWidget,QLabel
from pathlib import Path
import matplotlib.ticker as ticker
import numpy as np
import pandas as pd
import seaborn as sns
from sklearn.preprocessing import StandardScaler
import flowkit as fk
from matplotlib.backends.backend_qt5agg import FigureCanvas
from matplotlib.figure import Figure
import os
from docs.layouts import Ui_appMainWindow
from docs.functions import cr_df, tsne # type: ignore

class MainWindow(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.w = None
        
        self.ui = Ui_appMainWindow()
        self.ui.setupUi(self)

        self.ui.file_browse.clicked.connect(self.open_file_dialog)
        self.ui.comp_browse.clicked.connect(self.comp_file_dialog)
        self.ui.file_browse_cl.clicked.connect(self.cl_file)
        self.ui.comp_browse_cl.clicked.connect(self.cl_comp)
        self.ui.Next_but.clicked.connect(self.forward_button_clicked)
        self.ui.Run_but.clicked.connect(self.run_button_clicked)
        

        if not os.path.exists('temp'):
            os.mkdir('temp')
            
        if not os.path.exists('Results'):
            os.mkdir('Results')
        
        self.show()
   
    def open_file_dialog(self):
        filenames, _ = QFileDialog.getOpenFileNames(
            self,
            "Select Files",
            "C:/Users",
            "FCS files (*.fcs)"
        )
        if filenames:
            self.ui.file_list.addItems([str(Path(filename))
                                     for filename in filenames])      
            
    def comp_file_dialog(self):
        filename, _ = QFileDialog.getOpenFileName(
            self,
            "Select File",
            "C:/Users",
            "FCS file (*.fcs)"
        )
        if filename:
            self.ui.comp_list.addItems([str(Path(filename))])
            
    def cl_file(self):
        self.ui.file_list.clear() 
        
    def cl_comp(self):
        self.ui.comp_list.clear() 

    def forward_button_clicked(self):
        
        comp_c = self.ui.comp_list.count()
        
        pop = []
        for index in range(self.ui.file_list.count()):
            pop.append(self.ui.file_list.item(index).text())
        
        dsp = int(self.ui.Down.text())
        
        if comp_c!=0:
            s1 = fk.Sample(self.ui.comp_list.item(0).text())
            comp = s1.metadata['spill']
        else:
            comp = 0


        Xn = cr_df(pop, comp_c,dsp,comp)

        
        self.tr = Xn
        self.ui.listWidget.clear() 
        for i in Xn.columns:
            item = QListWidgetItem(str(i))
            self.ui.listWidget.addItem(item)
        
    def run_button_clicked(self):
        
        out = self.ui.outp.text()
        
        val = []
        for i in self.ui.listWidget.selectedItems():
            val.append(i.text())
            
        px = int(self.ui.Pr.text())
        it = int(self.ui.it.text())

        Xn = self.tr

        Xnn = tsne(Xn,val,px,it)

        Xnn.to_pickle("Results/"+str(out)+".pkl")
        Xnn.to_pickle("temp/_temp.pkl")
        
        if self.w is None:
            self.w = AnotherWindow()
        self.w.show()

class AnotherWindow(QWidget):


    def __init__(self):
        super().__init__()
        layout = QGridLayout()
        self.label = QLabel("Success!!!")
        layout.addWidget(self.label,0,0)
        self.setLayout(layout)
        
        
        Xn = pd.read_pickle("temp/_temp.pkl")
        os.remove("temp/_temp.pkl")
        
        self.canvas = FigureCanvas(Figure(figsize=(12, 6), dpi=300))
        ax = self.canvas.figure.subplots(nrows=1, ncols=2)
        sns.scatterplot(x='tsne_1', y='tsne_2', data=Xn, ax=ax[0],s=5)
        sns.kdeplot(x='tsne_1', y='tsne_2', data=Xn, ax=ax[1],shade=True, thresh = 0.05, color = 'black')

        ax[0].set_aspect('equal')
        ax[1].set_aspect('equal')
        ax[0].xaxis.set_major_locator(ticker.NullLocator())
        ax[0].yaxis.set_major_locator(ticker.NullLocator())
        ax[1].xaxis.set_major_locator(ticker.NullLocator())
        ax[1].yaxis.set_major_locator(ticker.NullLocator())
        
        
        layout.addWidget(self.canvas,1,0)
        self.canvas.draw()
        
        
        self.savefig_button = QPushButton('Save Figure')
        layout.addWidget(self.savefig_button,2,0)    
        
        self.savefig_button.clicked.connect(self.savefig)
        
    def savefig(self):
         
        # selecting file path
        filePath, _ = QFileDialog.getSaveFileName(self, "Save Image", "",
                         "PNG(*.png);;JPEG(*.jpg *.jpeg);;All Files(*.*) ")
 
        # if file path is blank return back
        if filePath == "":
            return
         
        # saving canvas at desired path
        self.canvas.print_figure(filePath)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = MainWindow()
    sys.exit(app.exec())
    

    