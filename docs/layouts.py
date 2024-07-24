from PyQt5.QtWidgets import QApplication,QSlider,QComboBox,QAbstractItemView, QGridLayout, QLineEdit, QPushButton,QButtonGroup, QListWidget,QLabel, QRadioButton
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg, FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
from PyQt5.QtCore import Qt

class Ui_appMainWindow(object):
    
    def setupUi(self, MainWindow):
        MainWindow.setWindowTitle('t-SNE analysis')
        MainWindow.setGeometry(100, 100, 400, 700)
        layout = QGridLayout()
        MainWindow.setLayout(layout)

        
        self.listWidget = QListWidget()
        self.listWidget.setSelectionMode(
            QAbstractItemView.ExtendedSelection
        )


        # file selection
        self.file_browse = QPushButton('Select samples')
    
        
        self.comp_browse = QPushButton('Select compensation file')

        
        self.file_browse_cl = QPushButton('Clear')
        self.comp_browse_cl = QPushButton('Clear')
        
        
        self.Next_but= QPushButton('Select parameters for clustering')
        
        self.file_list = QListWidget(MainWindow)
        self.comp_list = QListWidget(MainWindow)
        self.Down = QLineEdit(MainWindow)
        self.Pr = QLineEdit("30",MainWindow)
        self.it = QLineEdit("1000",MainWindow)
        
        self.outp = QLineEdit(MainWindow)
        
        self.Run_but= QPushButton('Run t-SNE')
        
    
        layout.addWidget(QLabel('Selected Files:'), 0, 0)
        layout.addWidget(self.file_list, 1, 0)
        layout.addWidget(self.file_browse, 2, 0)
        layout.addWidget(self.file_browse_cl, 3, 0)
        layout.addWidget(self.comp_list, 4, 0)
        layout.addWidget(self.comp_browse, 5, 0)
        layout.addWidget(self.comp_browse_cl, 6, 0)
        layout.addWidget(QLabel('Downsample size:'), 7, 0)
        layout.addWidget(self.Down, 8, 0)
        layout.addWidget(QLabel('Enter Perplexity:'), 9, 0)
        layout.addWidget(self.Pr, 10, 0)
        layout.addWidget(QLabel('Enter number of iterations:'), 11, 0)
        layout.addWidget(self.it, 12, 0)
        layout.addWidget(self.Next_but, 13, 0)
        layout.addWidget(self.listWidget, 14, 0)
        layout.addWidget(QLabel('Name output file:'), 15, 0)
        layout.addWidget(self.outp, 16, 0)
        layout.addWidget(self.Run_but, 17, 0)

class Ui_analysWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setWindowTitle('Result analysis')
        MainWindow.setGeometry(100, 100, 400, 100)
        layout = QGridLayout()
        MainWindow.setLayout(layout)

        self.inp = QListWidget(MainWindow)
        self.clr = QPushButton('Color t-SNE by values')
        
        self.sep = QPushButton('Plot each condition')
        
        self.sel = QPushButton('Compare conditions')
        
        self.delt = QPushButton('Clear selection')

        self.file_browse = QPushButton('Select file')

        self.tag = QPushButton('Create tags')
        
        
        layout.addWidget(QLabel('Name output file:'), 0, 0)
        layout.addWidget(self.inp, 1, 0)
        layout.addWidget(self.file_browse, 2, 0)
        layout.addWidget(self.delt, 3, 0)
        layout.addWidget(self.tag, 4, 0)
        layout.addWidget(self.clr, 5, 0)
        layout.addWidget(self.sep, 6, 0)
        layout.addWidget(self.sel, 7, 0)

class Ui_TagWindow(object):
    def setupUi(self, TagWindow):
        TagWindow.setWindowTitle('Tagging')
        TagWindow.setGeometry(100, 100, 400, 100)
        layout = QGridLayout()
        TagWindow.setLayout(layout)

        self.inp = QListWidget(TagWindow)
        
        self.delt = QPushButton('Clear selection')
        self.file_browse = QPushButton('Select file')
        
        
        layout.addWidget(QLabel('Name file for tagging:'), 0, 0)
        layout.addWidget(self.inp, 1, 0)
        layout.addWidget(self.file_browse, 2, 0)
        layout.addWidget(self.delt, 3, 0)


class Ui_S_a_Window(object):

    def setupUi(self, SepWindow):
        
        layout = QGridLayout()

        SepWindow.setLayout(layout)
        

        self.cb_platform = QComboBox(SepWindow)
        
            
        self.gr_list = QListWidget(SepWindow)
        self.adt = QPushButton('Add condition')
        self.dl = QPushButton('Delete condition')
        self.plt1 = QPushButton('Plot (Group 1)')
        self.plt2 = QPushButton('Plot (Group 2)')

        self.p1=QButtonGroup()
        self.rb_kde1 = QRadioButton('KDE plot')
        self.rb_scat1 = QRadioButton('Scatter plot')
        self.p1.addButton(self.rb_kde1)
        self.p1.addButton(self.rb_scat1)

        self.p2=QButtonGroup()
        self.rb_kde2 = QRadioButton('KDE plot')
        self.rb_scat2 = QRadioButton('Scatter plot')
        self.p2.addButton(self.rb_kde2)
        self.p2.addButton(self.rb_scat2)


            
        layout.addWidget(QLabel('Select graph of interest (Group 1):'), 0, 0)
        layout.addWidget(self.cb_platform, 1, 0)
        layout.addWidget(self.gr_list, 2, 0)
        layout.addWidget(self.adt, 3, 0)
        layout.addWidget(self.dl, 4, 0)
        layout.addWidget(self.rb_kde1, 5, 0)
        layout.addWidget(self.rb_scat1, 6, 0)
        layout.addWidget(self.plt1, 7, 0)
        
        self.save_button = QPushButton('Save')
        layout.addWidget(self.save_button,9,0)
        
        
        self.save_button2 = QPushButton('Save')
        layout.addWidget(self.save_button2,9,1)
    
        
        self.cb_platform2 = QComboBox(SepWindow)

            
        self.gr_list2 = QListWidget(SepWindow)
        self.adt2 = QPushButton('Add condition')
        self.dl2 = QPushButton('Delete condition')
            
        layout.addWidget(QLabel('Select graph of interest (Group 2):'), 0, 1)
        layout.addWidget(self.cb_platform2, 1, 1)
        layout.addWidget(self.gr_list2, 2, 1)
        layout.addWidget(self.adt2, 3, 1)
        layout.addWidget(self.dl2, 4, 1)
        layout.addWidget(self.rb_kde2, 5, 1)
        layout.addWidget(self.rb_scat2, 6, 1)
        layout.addWidget(self.plt2, 7, 1)
        

        self.canvas1 = FigureCanvas(Figure(dpi = 150))
        layout.addWidget(self.canvas1, 8,0)
        
        self.canvas2 = FigureCanvas(Figure(dpi = 150))
        layout.addWidget(self.canvas2, 8,1)

class Ui_C_a_Window(object):
    def setupUi(self, CompareWindow):
        
        layout = QGridLayout()

        CompareWindow.setLayout(layout)
        CompareWindow.setGeometry(100, 100, 400, 1000)
        
        self.rb_kde = QRadioButton('KDE plot',CompareWindow)
        self.rb_scat = QRadioButton('Scatter plot',CompareWindow)
        self.rb_kde.setEnabled(True)

        self.cb_platform = QComboBox(CompareWindow)

        self.slider_x = QSlider(Qt.Orientation.Horizontal, CompareWindow)
        self.slider_x.setRange(0, 100)      
        self.slider_x.setValue(50) 
        self.slider_y = QSlider(Qt.Orientation.Horizontal, CompareWindow)
        self.slider_y.setRange(0, 100) 
        self.slider_y.setValue(50) 
        self.slider_w = QSlider(Qt.Orientation.Horizontal, CompareWindow)
        self.slider_w.setRange(0, 100)
        self.slider_w.setValue(50)
        self.slider_h = QSlider(Qt.Orientation.Horizontal, CompareWindow)
        self.slider_h.setRange(0, 100)
        self.slider_h.setValue(50)
        self.slider_phi = QSlider(Qt.Orientation.Horizontal, CompareWindow)
        self.slider_phi.setRange(0, 180)
    

        
        self.save_but= QPushButton('Add condition')

        
        self.dist_but= QPushButton('Plot distributions')

        
        self.figure = plt.figure(dpi = 150)
        self.canvas1 = FigureCanvasQTAgg(self.figure)
        
        
        self.savefig_button = QPushButton('Save Figure')
        layout.addWidget(self.savefig_button,5,0) 

        self.savedat_button = QPushButton('Export Data')
        self.outp = QLineEdit(CompareWindow)
        
            
        layout.addWidget(QLabel('Select graph of interest:'), 0, 0)
        layout.addWidget(self.rb_kde, 1, 0)
        layout.addWidget(self.rb_scat, 2, 0)
        layout.addWidget(self.cb_platform, 3, 0)
        layout.addWidget(self.canvas1, 4,0)
        layout.addWidget(QLabel('Xc:'), 6, 0)
        layout.addWidget(self.slider_x, 7, 0)
        layout.addWidget(QLabel('Yc:'), 8, 0)
        layout.addWidget(self.slider_y, 9, 0)
        layout.addWidget(QLabel('Width:'), 10, 0)
        layout.addWidget(self.slider_w, 11, 0)
        layout.addWidget(QLabel('Height:'), 12, 0)
        layout.addWidget(self.slider_h, 13, 0) 
        layout.addWidget(QLabel('Angle:'), 14, 0)
        layout.addWidget(self.slider_phi, 15, 0)
        layout.addWidget(self.outp, 16, 0)
        layout.addWidget(self.save_but, 17, 0)
        layout.addWidget(self.dist_but, 18, 0)
        layout.addWidget(self.savedat_button,19,0)

class Ui_D_a_Window(object):
    def setupUi(self, DistWindow):
        
        layout = QGridLayout()

        DistWindow.setLayout(layout)
        DistWindow.setGeometry(100, 100, 800, 1000)
        
        self.cb_platform = QComboBox(DistWindow)
        self.cb2_platform = QComboBox(DistWindow)
        self.cb3_platform = QComboBox(DistWindow)
        
           
        layout.addWidget(QLabel('Select parameter of interest :'), 0, 0)
        layout.addWidget(self.cb_platform, 1, 0)
        layout.addWidget(QLabel('Select axis for dotplot :'), 5, 0)
        layout.addWidget(self.cb2_platform, 6, 0)
        layout.addWidget(self.cb3_platform, 7, 0)
        self.canvas = FigureCanvas(Figure(dpi = 150))
        layout.addWidget(self.canvas, 2,0)
        
        self.canvas2 = FigureCanvas(Figure(dpi = 150))
        layout.addWidget(self.canvas2, 8,0)
        
        self.savefig1_button = QPushButton('Save Figure')
        layout.addWidget(self.savefig1_button,3,0)

        self.heat_button = QPushButton('Plot heatmap')
        layout.addWidget(self.heat_button,4,0)

        self.savefig2_button = QPushButton('Save Figure')
        layout.addWidget(self.savefig2_button,9,0)
        
        
