import matplotlib.pyplot as plt
from matplotlib.offsetbox import OffsetImage, AnnotationBbox
from PIL import Image
import matplotlib.image as image
import numpy as np


class MazeDrawer:
    def __init__(self, agentX, agentY, mummyX, mummyY, scX, scY, onkey, game, step, action):
        self.__agentX = agentX
        self.__agentY = agentY
        self.__mummyX = mummyX
        self.__mummyY = mummyY
        self.__scX = scX
        self.__scY = scY
        self.vwall = [(0, 4), (1, 6), (1, 8), (3, 8), (4, 6), (5, 3), (5, 8), (7, 0), (7, 4), (7, 5), (7, 7), (8, 3),
                      (8, 5), (9, 0)]
        self.hwall = [(0, 0), (0, 7), (0, 8), (1, 3), (2, 4), (2, 7), (3, 4), (3, 7), (4, 3), (4, 8), (5, 2), (6, 2),
                      (7, 3), (7, 8), (7, 9), (8, 1), (8, 4), (7, 2)]
        self.__onkey = onkey

        self.__game = game
        self.__step = step
        self.__action = action
    # 画线
    def __drawLine(self, x1, y1, x2, y2):
        plt.plot([x1, x2], [y1, y2], color='black')

    # 画形状
    def __drawShape(self, x, y, shape, color):
        m = y + 0.5
        n = x + 0.5
        plt.scatter(m, n, s=1300, marker=shape, color=color)

    # 画背景
    def __drawBackground(self):
        plt.figure(figsize=(10, 10))
        # 画网格线
        for i in range(1, 10):
            plt.plot([i, i], [0, 10], color='AntiqueWhite')
        for i in range(0, 10):
            plt.plot([0, 10], [i, i], color='AntiqueWhite')
        # 画边界
        plt.plot([0, 10], [0, 0], color='black')
        plt.plot([10, 10], [0, 10], color='black')
        plt.plot([0, 10], [10, 10], color='black')
        plt.plot([0, 0], [10, 0], color='black')
        # 画横墙
        for cell in self.hwall:
            self.__drawLine(cell[1], cell[0] + 1, cell[1] + 1, cell[0] + 1)
        # 画竖墙
        for cell in self.vwall:
            self.__drawLine(cell[1] + 1, cell[0], cell[1] + 1, cell[0] + 1)
        # 画出口
        trap = plt.Rectangle((4, 3), 1, 1, fc='red')
        plt.gca().add_patch(trap)
        # 画陷阱
        exit = plt.Rectangle((5, 9), 1, 1, fc='green')
        plt.gca().add_patch(exit)

    # 画栅栏
    def __drawFence(self):
        if self.__onkey % 2 != 0:
            plt.plot([2, 3], [8, 8], color='AntiqueWhite')

    # 画钥匙
    def __drawKey(self):
        Image = image.imread('key.png')
        ax = plt.gca()
        im = OffsetImage(Image, zoom=0.08)
        im.image.axes = ax

        ab = AnnotationBbox(im, (9.5, 7.5), frameon=False)

        ax.add_artist(ab)
        ax.autoscale()

    # 绿色五角星（玩家）
    def __drawAgent(self):
        self.__drawShape(self.__agentX, self.__agentY, '*', 'green')

    # 红色圆形（木乃伊）
    def __drawMummy(self):
        self.__drawShape(self.__mummyX, self.__mummyY, 'o', 'pink')

    # 黄色三角形（蝎子）
    def __drawSc(self):
        self.__drawShape(self.__scX, self.__scY, '^', 'DarkOrange')

    # 打印标题
    def __printHead(self):
        plt.title("Game:{} Step:{} Action:{}".format(self.__game, self.__step, self.__action), fontsize=16)
    def saveFrame(self, step):
        # fig = plt.figure()
        # ax = plt.axes(xlim=(0, 9), ylim=(0, 9))
        self.__drawBackground()
        self.__drawAgent()
        self.__drawMummy()
        self.__drawKey()
        self.__drawFence()
        self.__printHead()
        if ((self.__scX, self.__scY)!=(self.__mummyX, self.__mummyY)):
            self.__drawSc()
        plt.gca().invert_yaxis()
        plt.axis('off')
        plt.savefig('maze_{0:03}.png'.format(step))
