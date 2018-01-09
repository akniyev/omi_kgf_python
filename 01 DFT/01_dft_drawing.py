import sys
import numpy as np
from math import *

from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLineEdit, QLabel

from MultiPlot2d import MultiPlot2d

if __name__ == "__main__":
    app = QApplication(sys.argv)

    plot = MultiPlot2d()
    plot.add_plot('f', color=(0, 0, 0))
    plot.add_plot('restored', color=(255, 0, 0))
    plot.show()

    # Create a window with controls

    wnd = QWidget()
    vbox = QVBoxLayout()
    wnd.setLayout(vbox)

    txt_n = QLineEdit("n=")
    txt_n.setText("4")
    lbl_n = QLabel("n = ")

    txt_D = QLineEdit("D =")
    txt_D.setText("2048")
    lbl_D = QLabel("D = ")

    txt_N = QLineEdit("N =")
    txt_N.setText("8")
    lbl_N = QLabel("N")

    btn_calculate = QPushButton("Calculate")

    vbox.addWidget(lbl_n)
    vbox.addWidget(txt_n)

    vbox.addWidget(lbl_N)
    vbox.addWidget(txt_N)

    vbox.addWidget(lbl_D)
    vbox.addWidget(txt_D)

    vbox.addWidget(btn_calculate)

    wnd.setGeometry(10, 10, 300, 100)
    wnd.show()

    # -----------------------

    def draw():
        N = int(txt_N.text())
        n = int(txt_n.text())
        D = int(txt_D.text())

        tj = lambda i: 2 * pi * i / N - pi
        f = lambda x: abs(x)

        a = [f(tj(i)) for i in range(N)]

        b = [c / N for c in np.fft.fft(a)]

        b_dense = [complex(0, 0)] * D

        b_dense[0] = b[0]
        for i in range(1, n):
            b_dense[i] = b[i]
            b_dense[D - i] = b[N - i]

        if N // 2 == n:
            b_dense[N // 2] = b[N // 2] / 2
            b_dense[D - N // 2] += b[N // 2] / 2

        b_dense = [c * D for c in b_dense]

        a_dense = [a.real for a in np.fft.ifft(b_dense)]



        xs = [-pi + 2 * pi / D * i for i in range(D + 1)]
        ys = [f(x) for x in xs]

        a_dense.append(a_dense[0])

        plot.set_plot_data('f', xs, ys)
        plot.set_plot_data('restored', xs, a_dense)


        plot.refresh()

    btn_calculate.pressed.connect(draw)

    sys.exit(app.exec_())