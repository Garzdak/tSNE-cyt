"""Analysis of tSNE plot, obtained in perform_tsne file"""
import sys
import os
from pathlib import Path
from PyQt5.QtWidgets import (
    QApplication, QFileDialog,QComboBox, QWidget, QGridLayout, QPushButton,
    QLabel,QCheckBox, QLineEdit,QVBoxLayout, QFormLayout, QHBoxLayout
    )
import matplotlib.ticker as ticker
import numpy as np
import pandas as pd
import seaborn as sns
from matplotlib.backends.backend_qt5agg import FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
from matplotlib.pyplot import cm
from matplotlib.patches import Ellipse
import xlsxwriter
from docs.layouts import Ui_analysWindow, Ui_S_a_Window, Ui_C_a_Window, Ui_D_a_Window

class MainWindow(QWidget):
    """Main window of analysis of tSNE plot"""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.w = None
        self.w1 = None
        self.w2 = None
        self.w3 = None
        self.ui = Ui_analysWindow()
        self.ui.setupUi(self)
        self.ui.clr.clicked.connect(self.gr_val)
        self.ui.sep.clicked.connect(self.sep_gr)
        self.ui.sel.clicked.connect(self.comp_c)
        self.ui.delt.clicked.connect(self.delt_f)
        self.ui.tag.clicked.connect(self.tags)
        self.ui.file_browse.clicked.connect(self.open_file_dialog)
        if not os.path.exists('temp'):
            os.mkdir('temp')
        if not os.path.exists('temp dist'):
            os.mkdir('temp dist')
        try:
            os.remove('temp/_temp2.pkl')
        except FileNotFoundError:
            pass
        self.show()

    def open_file_dialog(self):
        """Open results of tSNE"""
        filename, _ = QFileDialog.getOpenFileName(
            self,
            "Select File",
            "C:/Users/10053684/Desktop/Play/Fragmented program",
            "Pickle file (*.pkl)"
        )
        if filename:
            self.ui.inp.addItems([str(Path(filename))])
        x1 = pd.read_pickle(self.ui.inp.item(0).text())
        x1.to_pickle("temp/_temp2.pkl")
    def tags(self):
        """Open window for tag creation"""
        self.w3 = TagWindow()
        self.w3.show()
    def delt_f(self):
        """Clear selection of file"""
        self.ui.inp.clear()
    def gr_val(self):
        """Open window for coloring by value"""
        self.w = ColorWindow()
        self.w.show()
    def sep_gr(self):
        """Open window for sample comparison"""
        self.w1 = SepWindow()
        self.w1.show()
    def comp_c(self):
        """Open Compare window for area comparison"""
        self.w2 = CompareWindow()
        self.w2.show()

class TagWindow(QWidget):
    """Create tag, grouping several samples"""
    def __init__(self):
        super().__init__()
        self.xn = pd.read_pickle("temp/_temp2.pkl")
        self.smpl = self.xn['id'].unique()
        self.setWindowTitle("Tagging")
        self.controls = []
        save_but = QPushButton('Save', self)
        save_but.clicked.connect(self.save)
        self.outp = QLineEdit(self)
        vbox = QVBoxLayout()
        formlayout = QFormLayout()
        vbox.addLayout(formlayout)
        hbox = QHBoxLayout()
        vbox.addLayout(hbox)
        vbox.addWidget(QLabel("Name the tagged file"))
        vbox.addWidget(self.outp)
        vbox.addWidget(save_but)
        self.setLayout(vbox)
        self.formlayout = formlayout
        for smpl_val in self.smpl:
            edit = QLineEdit(self)
            self.controls.append(edit)
            self.formlayout.addRow(str(smpl_val), edit)
    def save(self):
        """Save tags into file"""
        out = self.outp.text()
        values = [x.text() for x in self.controls]
        dictionary = dict(zip(self.smpl, values))
        xnn = self.xn.copy()
        xnn['tag'] = xnn['id'].map(dictionary)
        xnn.to_pickle("Results/"+str(out)+".pkl")

class ColorWindow(QWidget):
    """Color tSNE plot by parameter of interest"""
    def __init__(self):
        super().__init__()
        layout = QGridLayout()
        self.setLayout(layout)
        xn = pd.read_pickle("temp/_temp2.pkl")
        itm = xn.columns
        self.cb_platform = QComboBox(self)
        for i in itm:
            self.cb_platform.addItem(i)
        layout.addWidget(QLabel('Select parameter:'), 0, 0)
        layout.addWidget(self.cb_platform, 1, 0)
        self.cb_platform.activated.connect(self.draw)
        self.tr = xn
        self.canvas = FigureCanvas(Figure(dpi = 150))
        layout.addWidget(self.canvas)
        self.save_button = QPushButton('Save')
        layout.addWidget(self.save_button)
        self.save_button.clicked.connect(self.save)
    def save(self):
        """Save plot"""
        # selecting file path
        filepath, _ = QFileDialog.getSaveFileName(self, "Save Image", "",
                         "PNG(*.png);;JPEG(*.jpg *.jpeg);;All Files(*.*) ")
        # if file path is blank return back
        if filepath == "":
            return
        # saving canvas at desired path
        self.canvas.print_figure(filepath)
    def draw(self):
        """Draw plot colored by parameter"""
        xn = self.tr
        col = self.cb_platform.currentText()
        y = np.ravel(xn[col].values.tolist())
        self.canvas.figure.clf()
        with plt.style.context("ggplot"):
            tsne_result_df = pd.DataFrame({'tsne_1': xn['tsne_1'].values.tolist(),
                                           'tsne_2': xn['tsne_2'].values.tolist(), 'label': y})
            ax = self.canvas.figure.subplots()
            sns.scatterplot(x='tsne_1', y='tsne_2', hue='label', data=tsne_result_df, ax=ax,
                            s=5, palette = "icefire",alpha = 0.7)
            ax.set_aspect('equal')
            ax.legend(bbox_to_anchor=(1.05, 1,), loc=2,
                      borderaxespad=0.0, framealpha=0.99,markerscale=5)
            ax.xaxis.set_major_locator(ticker.NullLocator())
            ax.yaxis.set_major_locator(ticker.NullLocator())
            self.canvas.draw()

class SepWindow(QWidget):
    """Compare samples from different groups"""
    def __init__(self):
        super().__init__()

        self.s_ui = Ui_S_a_Window()
        self.s_ui.setupUi(self)
        xn = pd.read_pickle("temp/_temp2.pkl")
        pop = xn['id'].unique().tolist()

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
        self.tr = xn
    def save(self):
        """Add samples to group"""
        # selecting file path
        filepath, _ = QFileDialog.getSaveFileName(self, "Save Image", "",
                         "PNG(*.png);;JPEG(*.jpg *.jpeg);;All Files(*.*) ")
        # if file path is blank return back
        if filepath == "":
            return
        # saving canvas at desired path
        self.s_ui.canvas1.print_figure(filepath)
    def save2(self):
        """Save plot"""
        # selecting file path
        filepath, _ = QFileDialog.getSaveFileName(self, "Save Image", "",
                         "PNG(*.png);;JPEG(*.jpg *.jpeg);;All Files(*.*) ")
        # if file path is blank return back
        if filepath == "":
            return
        # saving canvas at desired path
        self.s_ui.canvas2.print_figure(filepath)
    def adtt(self):
        """Add samples to group"""
        self.s_ui.gr_list.addItems([self.s_ui.cb_platform.currentText()])
    def dll(self):
        """Delete items from list"""
        list_items=self.s_ui.gr_list.selectedItems()
        if not list_items:
            return
        for item in list_items:
            self.s_ui.gr_list.takeItem(self.s_ui.gr_list.row(item))
    def adtt2(self):
        """Add samples to group"""
        self.s_ui.gr_list2.addItems([self.s_ui.cb_platform2.currentText()])
    def dll2(self):
        """Delete items from list"""
        list_items=self.s_ui.gr_list2.selectedItems()
        if not list_items:
            return
        for item in list_items:
            self.s_ui.gr_list2.takeItem(self.s_ui.gr_list2.row(item))
    def dr1(self):
        """Draw selected tSNE plots"""
        xn = self.tr
        pop = []
        for index in range(self.s_ui.gr_list.count()):
            pop.append(self.s_ui.gr_list.item(index).text())

        self.s_ui.canvas1.figure.clf()
        ax = self.s_ui.canvas1.figure.subplots(nrows=1, ncols=len(pop))
        j=0
        for i in pop:
            xctr = xn.loc[xn['id'] == i]
            if len(pop)>1:
                if self.s_ui.rb_kde1.isChecked():
                    sns.kdeplot(x='tsne_1', y='tsne_2', data=xctr, ax=ax[j],
                                fill=True, thresh = 0.01, color = 'red')
                if self.s_ui.rb_scat1.isChecked():
                    sns.scatterplot(x='tsne_1', y='tsne_2', data=xctr, ax=ax[j],s=5)
                ax[j].set_title(i)
                ax[j].set_aspect('equal')
                ax[j].xaxis.set_major_locator(ticker.NullLocator())
                ax[j].yaxis.set_major_locator(ticker.NullLocator())
                j+=1
            elif len(pop)==1:
                if self.s_ui.rb_kde1.isChecked():
                    sns.kdeplot(x='tsne_1', y='tsne_2', data=xctr, ax=ax,
                                fill=True, thresh = 0.01, color = 'red')
                if self.s_ui.rb_scat1.isChecked():
                    sns.scatterplot(x='tsne_1', y='tsne_2', data=xctr, ax=ax,s=5)
                ax.set_title(i)
                ax.set_aspect('equal')
                ax.xaxis.set_major_locator(ticker.NullLocator())
                ax.yaxis.set_major_locator(ticker.NullLocator())
        self.s_ui.canvas1.draw()
    def dr2(self):
        """Draw selected tSNE plots"""
        xn = self.tr
        pop = []
        for index in range(self.s_ui.gr_list2.count()):
            pop.append(self.s_ui.gr_list2.item(index).text())
        self.s_ui.canvas2.figure.clf()
        ax = self.s_ui.canvas2.figure.subplots(nrows=1, ncols=len(pop))
        j=0
        for i in pop:
            xctr = xn.loc[xn['id'] == i]
            if len(pop)>1:
                if self.s_ui.rb_kde2.isChecked():
                    sns.kdeplot(x='tsne_1', y='tsne_2', data=xctr, ax=ax[j],
                                fill=True, thresh = 0.01, color = 'red')
                if self.s_ui.rb_scat2.isChecked():
                    sns.scatterplot(x='tsne_1', y='tsne_2', data=xctr, ax=ax[j],s=5)
                ax[j].set_title(i)
                ax[j].set_aspect('equal')
                ax[j].xaxis.set_major_locator(ticker.NullLocator())
                ax[j].yaxis.set_major_locator(ticker.NullLocator())
            elif len(pop)==1:
                if self.s_ui.rb_kde2.isChecked():
                    sns.kdeplot(x='tsne_1', y='tsne_2', data=xctr, ax=ax,
                                fill=True, thresh = 0.01, color = 'red')
                if self.s_ui.rb_scat2.isChecked():
                    sns.scatterplot(x='tsne_1', y='tsne_2', data=xctr, ax=ax,s=5)
                ax.set_title(i)
                ax.set_aspect('equal')
                ax.xaxis.set_major_locator(ticker.NullLocator())
                ax.yaxis.set_major_locator(ticker.NullLocator())
            j+=1
        self.s_ui.canvas2.draw()

class CompareWindow(QWidget):
    """Window for comparing different areas of tSNE plot"""
    def __init__(self):
        super().__init__()
        self.c_ui = Ui_C_a_Window()
        self.c_ui.setupUi(self)

        xn = pd.read_pickle("temp/_temp2.pkl")
        pop = xn['id'].unique().tolist()

        for i in pop:
            self.c_ui.cb_platform.addItem(i)

        self.c_ui.cb_platform.addItem("Whole t-SNE")
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
        self.tr = xn
        self.plots = []
        self.names = []
        self.slg = None
        self.xlms = None
        self.ylms = None
        self.h = None
        self.w = None
        self.w3 = None
        self.w4 = None

        self.ellipse = Ellipse(
            xy=(self.x, self.y),
            width=self.w,
            height=self.h,
            angle=0,
            facecolor="none",
            edgecolor="b"
            )
        self.x_el = 50
        self.y_el = 50
        self.w_el = 50
        self.h_el = 50
        self.phi_el = 0

    def savefig(self):
        """Save plot with ellipse of selection"""
        # selecting file path
        filepath, _ = QFileDialog.getSaveFileName(self, "Save Image", "",
                         "PNG(*.png);;JPEG(*.jpg *.jpeg);;All Files(*.*) ")
        # if file path is blank return back
        if filepath == "":
            return
        # saving canvas at desired path
        self.c_ui.canvas1.print_figure(filepath)

    def savedat(self):
        """Save data into an Excel file"""
        # selecting file path
        filepath, _ = QFileDialog.getSaveFileName(self, "Export data", "",
                         "xlsx(*.xlsx)")
        # if file path is blank return back
        if filepath == "":
            return
        workbook = xlsxwriter.Workbook(filepath)
        cl_nm = list(self.plots[0].columns)

        # saving plots at desired path
        for i, plots_val in enumerate(self.plots):
            worksheet = workbook.add_worksheet(self.names[i])
            for j, cl_nm_val in enumerate(cl_nm):
                row = 1
                worksheet.write(0, j+1, cl_nm_val)
                l_pl = plots_val[cl_nm_val].to_list()
                for item in l_pl:
                    worksheet.write(row, j+1, item)
                    row += 1
        workbook.close()

    def dr1(self):
        """Draw plot for selecting area of interest"""
        xn = self.tr
        pop = self.c_ui.cb_platform.currentText()
        
        self.c_ui.canvas1.figure.clf()
        self.ax = self.c_ui.figure.subplots()

        if pop == "Whole t-SNE":
            xctr = xn.copy()
        else:
            xctr = xn.loc[xn['id'] == pop]
        self.slg = xctr


        if self.c_ui.rb_kde.isChecked():
            sns.kdeplot(x='tsne_1', y='tsne_2', data=xctr, ax=self.ax,
                        fill=True, thresh = 0.01, color = 'red')
        if self.c_ui.rb_scat.isChecked():
            sns.scatterplot(x='tsne_1', y='tsne_2', data=xctr, ax=self.ax,s=5)
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
        """Update ellipse patch"""
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
        """Update center x-coord"""
        self.ellipse.remove()
        self.x_el = value
        self.x = self.xlms[0]+self.x_el*(self.xlms[1]-self.xlms[0])/100
        self.update()
    def el_y(self, value):
        """Update center y-coord"""
        self.ellipse.remove()
        self.y_el = value
        self.y = self.ylms[0]+self.y_el*(self.ylms[1]-self.ylms[0])/100
        self.update()
    def el_w(self, value):
        """Update width"""
        self.ellipse.remove()
        self.w_el = value
        self.w = self.w_el*(self.xlms[1]-self.xlms[0])/100/2
        self.update()
    def el_h(self, value):
        """Update height"""
        self.ellipse.remove()
        self.h_el = value
        self.h = self.h_el*(self.ylms[1]-self.ylms[0])/100/2
        self.update()
    def el_phi(self, value):
        """Update angle"""
        self.ellipse.remove()
        self.phi_el = value
        self.update()
    def inellipse(self,x, y):
        """Check if dot in ellipse"""
        theta = self.phi_el*np.pi/180
        xr = x - self.x
        yr = y-self.y
        x0 = np.cos(theta)*xr + np.sin(theta)*yr
        y0 = -np.sin(theta)*xr + np.cos(theta)*yr
        p = (pow(x0, 2)/pow(self.w, 2)) + (pow(y0, 2)/pow(self.h, 2))
        return p<1
    def save(self):
        """Save area selection"""
        xn = self.tr
        pop = self.c_ui.cb_platform.currentText()

        if pop == "Whole t-SNE":

            xctr = xn.copy()
        else:
            xctr = xn.loc[xn['id'] == pop]
        self.slg = xctr
        x1 = xctr.copy()
        x1['p'] = list(map(self.inellipse, x1['tsne_1'], x1['tsne_2']))
        _plot = x1[x1['p'] == True]
        _out = self.c_ui.outp.text()
        self.plots.append(_plot)
        self.names.append(_out)
        self.w4 = SucWindow()
        self.w4.show()
    def dist(self):
        """Save distribution data and open new window"""
        for i, plots_val in enumerate(self.plots):
            plots_val.to_pickle('temp dist/'+str(i)+'.pkl')
        df_n = pd.DataFrame(self.names, columns=['Names'])
        df_n.to_pickle('temp dist/Names.pkl')
        self.w3 = DistWindow()
        self.w3.show()

class SucWindow(QWidget):
    """Success!!! message"""
    def __init__(self):
        super().__init__()
        layout = QGridLayout()

        self.setLayout(layout)
        layout.addWidget(QLabel('Success!!!'), 0, 0)

class DistWindow(QWidget):
    """Visualize distributions in the areas of interest"""
    def __init__(self):
        super().__init__()

        self.d_ui = Ui_D_a_Window()
        self.d_ui.setupUi(self)
        self.plots=[]
        self.names = pd.read_pickle('temp dist/Names.pkl')['Names'].to_list()

        os.remove('temp dist/Names.pkl')
        ct = len(os.listdir('temp dist'))
        for i in range(0,ct):
            n = 'temp dist/'+str(i)+'.pkl'
            self.plots.append(pd.read_pickle(n))
            os.remove(n)
        try:
            os.remove('temp/Heatmap.pkl')
        except FileNotFoundError:
            pass
        itm = (self.plots[0].columns).to_list()
        itm1 = itm[:-4]


        if 'id' in itm1:
            itm1.remove('id')
            
        for i in itm1:
            self.d_ui.cb_platform.addItem(i)
            self.d_ui.cb2_platform.addItem(i)
            self.d_ui.cb3_platform.addItem(i)
        self.d_ui.cb_platform.addItem("Number of events")

        if 'tag' in itm:
            self.d_ui.cb_platform.addItem("Tag distribution")
        self.d_ui.cb_platform.activated.connect(self.draw)
        self.d_ui.cb2_platform.activated.connect(self.dotplot)
        self.d_ui.cb3_platform.activated.connect(self.dotplot)
        self.d_ui.savefig1_button.clicked.connect(self.savefig1)
        self.d_ui.savefig2_button.clicked.connect(self.savefig2)

        self.d_ui.heat_button.clicked.connect(self.heatmap)

        df_ls, self.n_a = [], []

        for i, plots_val in enumerate(self.plots):
            self.n_a.append(self.names[i])
            _u = plots_val.copy()
            _u = _u.drop('id', axis=1)
            _u = _u.drop('tsne_1', axis=1)
            _u = _u.drop('tsne_2', axis=1)
            _u = _u.drop('p', axis=1)
            _u = _u._get_numeric_data()
            df_ls.append(_u.median().to_frame())



        cnct = df_ls[0]
        for i in range(1,len(df_ls)):
            cnct = pd.concat([cnct, df_ls[i]], axis="columns")

        cnct.columns = self.n_a
        cnct = cnct.T

        cnct.to_pickle("temp/Heatmap.pkl")

        self.w4 = None
    def savefig1(self):
        """Save plot"""
        # selecting file path
        filepath, _ = QFileDialog.getSaveFileName(self, "Save Image", "",
                          "PNG(*.png);;JPEG(*.jpg *.jpeg);;All Files(*.*) ")
        # if file path is blank return back
        if filepath == "":
            return
        # saving canvas at desired path
        self.d_ui.canvas.print_figure(filepath)
    def savefig2(self):
        """Save plot"""
        # selecting file path
        filepath, _ = QFileDialog.getSaveFileName(self, "Save Image", "",
                          "PNG(*.png);;JPEG(*.jpg *.jpeg);;All Files(*.*) ")
        # if file path is blank return back
        if filepath == "":
            return
        # saving canvas at desired path
        self.d_ui.canvas2.print_figure(filepath)
    def draw(self):
        """Plot the distribution of interest"""
        col = self.d_ui.cb_platform.currentText()
        self.d_ui.canvas.figure.clf()
        self.d_ui.canvas.figure.set_tight_layout(True)
        ax = self.d_ui.canvas.figure.subplots()
        color = iter(cm.rainbow(np.linspace(0, 1, len(self.plots))))
        if col == "Number of events":
            ln = [len(x) for x in self.plots]
            n_e = {'Area': self.n_a, '# events': ln}
            df_n_e = pd.DataFrame(n_e)
            sns.barplot(df_n_e, y="Area", x="# events", ax = ax, hue="Area", legend=False)

        elif col == "Tag distribution":
            cnts = []
            for i, plots_val in enumerate(self.plots):
                _df = plots_val.value_counts("tag").to_frame()
                _df['ind'] = self.n_a[i]
                cnts.append(_df)
            res = pd.concat(cnts)
            res['tag']=res.index
            res = res.set_index('ind')

            groups = self.n_a
            t_lst = res['tag'].unique().tolist()
            nlst = []
            for i, t_lst_val in enumerate(t_lst):
                nlst.append([])
                for j, plots_val in enumerate(self.plots):
                    try:
                        nlst[i].append(plots_val['tag'].value_counts()[t_lst_val])
                    except:
                        nlst[i].append(0)

            ax.bar(groups, nlst[0])
            m = nlst[0]
            for i in range(1,len(t_lst)):
                ax.bar(groups, nlst[i], bottom = m)
                res_list = []
                for k in range(0, len(self.plots)):
                    res_list.append(m[k] + nlst[i][k])
                m = res_list
                ax.legend(t_lst,bbox_to_anchor=(1.01, 1), borderaxespad=0)
        else:
            for i, plots_val in enumerate(self.plots):
                c = next(color)
                sns.kdeplot(data=plots_val, x=col, ax = ax,
                            label = self.names[i], linewidth = 2, c= c)
                ax.legend(bbox_to_anchor=(1.01, 1), borderaxespad=0)

        self.d_ui.canvas.draw()

        
    def dotplot(self):
        """Plot the dotplot"""
        c1 = self.d_ui.cb2_platform.currentText()
        c2 = self.d_ui.cb3_platform.currentText()
        color = iter(cm.rainbow(np.linspace(0, 1, len(self.plots))))
        self.d_ui.canvas2.figure.clf()
        self.d_ui.canvas2.figure.set_tight_layout(True)
        ax = self.d_ui.canvas2.figure.subplots()
        for i, plots_val in enumerate(self.plots):
            c = next(color)
            sns.scatterplot(x=c1, y=c2, data=plots_val, ax=ax,
                            s=3, color=c,label = self.names[i])
        ax.legend(bbox_to_anchor=(1.01, 1), borderaxespad=0, markerscale=5)
        self.d_ui.canvas2.draw()
    def heatmap(self):
        """Create heatmap button"""
        self.w4 = HeatWindow()
        self.w4.show()

class HeatWindow(QWidget):
    """Window for creating custom heatmap"""
    def __init__(self):
        super().__init__()
        layout = QGridLayout()
        self.setLayout(layout)
        self.cnct = pd.read_pickle("temp/Heatmap.pkl")

        col = self.cnct.columns.values.tolist()
        self.list_checkbox = col

        ordr = 0
        for i, v in enumerate(self.list_checkbox):
            self.list_checkbox[i] = QCheckBox(v)
            self.list_checkbox[i].setChecked(True)
            layout.addWidget(self.list_checkbox[i], i, 0)
            ordr = i

        self.canvas = FigureCanvas(Figure(tight_layout=True))
        layout.addWidget(self.canvas,ordr+1,0)
        self.plot_button = QPushButton('Plot heatmap')
        layout.addWidget(self.plot_button,ordr+2,0)
        self.savefig_button = QPushButton('Save Figure')
        layout.addWidget(self.savefig_button,ordr+3,0)
        self.savefig_button.clicked.connect(self.savefig)
        self.plot_button.clicked.connect(self.plot)
        
    def plot(self):
        """Plot heatmap"""
        chkd = []
        for i, v in enumerate(self.list_checkbox):
            if v.checkState():
                chkd.append(v.text())

        _cnct = self.cnct.copy()
        _cnct = _cnct[chkd]

        self.canvas.figure.clf()
        self.ax = self.canvas.figure.subplots(nrows=1, ncols=1)

        sns.heatmap(_cnct, cmap = 'hot', vmin = 0, vmax = 1, square=True,
                     ax = self.ax, xticklabels=1, yticklabels=1).set(xlabel='', ylabel='')

        self.canvas.draw()
    def savefig(self):
        """Saving heatmap plot"""
        # selecting file path
        filepath, _ = QFileDialog.getSaveFileName(self, "Save Image", "",
                         "PNG(*.png);;JPEG(*.jpg *.jpeg);;All Files(*.*) ")
        # if file path is blank return back
        if filepath == "":
            return
        # saving canvas at desired path
        self.canvas.print_figure(filepath)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = MainWindow()
    sys.exit(app.exec())

# End-of-file (EOF)
