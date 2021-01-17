import numpy as np
#地图大小
BOARD_ROWS = 10
BOARD_COLS = 10

#墙壁坐标
#阻挡了向右运动的竖直方向的墙
vwallR = [(0,4), (1,6), (1,8), (3,8), (4,6), (5,3), (5,8), (7,0), (7,4), (7,5), (7,7), (8,3), (8,5), (9,0)]
#阻挡了向下运动的水平方向的墙
hwallD = [(0,0), (0,7), (0,8), (1,3), (2,4), (2,7), (3,4), (3,7), (4,3), (4,8), (5,2), (6,2), (7,3), (7,8), (7,9), (8,1), (8,4), (7,2)]
#阻挡了向左运动的竖直方向的墙
vwallL = [(0, 5), (1, 7), (1, 9), (3, 9), (4, 7), (5, 4), (5, 9), (7, 1), (7, 5), (7, 6), (7, 8), (8, 4), (8, 6), (9, 1)]
#阻挡了向上运动的水平方向的墙
hwallU = [(1, 0), (1, 7), (1, 8), (2, 3), (3, 4), (3, 7), (4, 4), (4, 7), (5, 3), (5, 8), (6, 2), (7, 2), (8, 3), (8, 8), (8, 9), (9, 1), (9, 4), (8,2)]

#玩家起始坐标
playerStart = (3,1)
#木乃伊起始坐标
mummyStart = (5,8)
#蝎子起始坐标
scStart = (9,1)
#出口
win = (9,5)
#骷髅（陷阱）
trap = (3,4)
#钥匙所在处
key = (7,9)

#获得理想最短路径的函数
def idealRouteGenerator(mummyState, playerState):
    #足迹列表用来记录理想最短路径
    footprint = []
    #木乃伊和玩家的当前坐标
    mummyX, mummyY = mummyState
    playerX, playerY = playerState

    #玩家在木乃伊的相对方位
    Right = True if (playerX >= mummyX) else False
    Down = True if (playerY >= mummyY) else False

    #根据相对方位得出每次增加/减少的量
    incrementX = 1 if Right else -1
    incrementY = 1 if Down else -1

    #创建一个临时变量用来和玩家坐标靠近
    x, y = mummyX, mummyY

    # 理想情况
    #进行增加或减少直到纵坐标和玩家相同
    while y != playerY:
        y += incrementY
        footprint.append((x, y))

    # 进行增加或减少直到横坐标和玩家相同
    while x != playerX:
        x += incrementX
        footprint.append((x, y))

    return footprint

#在理想最短路径的基础上根据墙的位置得到最佳路径
def bestRouteGenerator(mummyState, playerState):
    #木乃伊和玩家的坐标
    mummyX, mummyY = mummyState
    playerX, playerY = playerState

    #先得到理想最短路径
    ideal = idealRouteGenerator(mummyState, playerState)

    i = 0
    final = []
    # 用一个临时列表存储当前的最佳路径
    tmp = ideal
    # 在开头插入起点，避免漏掉开头被卡住的情况
    tmp.insert(0, mummyState)
    # 因为这是在方格地图中，所以理想最佳步数中的总步数就是上界
    length = len(tmp)

    while i < length:
        # 判断当前行动的方向
        Right = True if (playerY > tmp[0][1]) else False
        Left = True if (playerY < tmp[0][1]) else False
        Down = True if (playerX > tmp[0][0]) else False
        Up = True if (playerX < tmp[0][0]) else False

        # 两种被卡住的情况
        # stuck1:在水平方向上被卡住
        stuck1 = True if ((Right and (tmp[0] in vwallR)) or (Left and (tmp[0] in vwallL))) else False
        # stuck2:在竖直方向上被卡住
        stuck2 = True if ((Up and (tmp[0] in hwallU)) or (Down and (tmp[0] in hwallD))) else False

        # 两个方向上都没被卡住
        if (not stuck1) and (not stuck2):
            # 在最终列表中记录这一步
            final.append(tmp[0])
            # 在临时最佳列表中删掉，让下一步成为第一个
            del tmp[0]

        # 在水平方向上被卡住而在竖直方向上是通畅的
        elif stuck1 and (not stuck2):
            # 记录下开头的这一步，不然会在后面tmp列表改变后丢失
            head = tmp[0]
            final.append(tmp[0])
            # 如果在整体方向上应该往上走
            if Up:
                # 向上平移一步，并得到新的最佳路径
                tmp = idealRouteGenerator((tmp[0][0] - 1, tmp[0][1]), playerState)
                # ideal函数生成的列表是不包含开头的，所以这里把开头补上
                tmp.insert(0, (head[0] - 1, head[1]))
            elif Down:
                # 向下平移一步，并得到新的最佳路径
                tmp = idealRouteGenerator((tmp[0][0] + 1, tmp[0][1]), playerState)
                tmp.insert(0, (head[0] + 1, head[1]))
            else:
                # 水平方向被卡住，并且目标在同一水平直线上，则保持不动（退出）
                break
        elif stuck2 and (not stuck1):
            head = tmp[0]
            final.append(tmp[0])
            if Left:
                tmp = idealRouteGenerator((tmp[0][0], tmp[0][1] - 1), playerState)
                tmp.insert(0, (head[0], head[1] - 1))
            elif Right:
                tmp = idealRouteGenerator((tmp[0][0], tmp[0][1] + 1), playerState)
                tmp.insert(0, (head[0], head[1] + 1))
            else:
                # 竖直方向被卡住，并且目标在同一竖直直线上，则保持不动（退出）
                break
        # 两个方向都被卡住
        else:
            final.append(tmp[0])
            break
        i += 1

    return final

#木乃伊的坐标专门用一个类来封装
class MUMMY_STATE():
    def __init__(self, state = mummyStart):
        self.state = state

#木乃伊的相关动作
class MUMMY:
    def __init__(self):
        self.State = MUMMY_STATE()

    # 根据最佳路径从而知道下一步怎么走
    def takeAction(self, playerState):
        #根据当前木乃伊和玩家的坐标得到最佳路径（包含当前坐标）
        self.final = bestRouteGenerator(self.State.state, playerState)

        #总步数在3步以上的话往后选两步
        if len(self.final) >= 3:
            return MUMMY_STATE(self.final[2])
        #总步数如果只有1，则选这一步；如果是2，则选择第二步
        else:
            return MUMMY_STATE(self.final[-1])
    #将木乃伊归还原位
    def reset(self):
        self.State = MUMMY_STATE()
    #执行动作，并更新坐标
    def play(self, playerState):
        self.State = self.takeAction(playerState)

#蝎子的坐标专门用一个类来封装
class SC_STATE():
    def __init__(self, state=scStart):
        self.state = state

#木乃伊的相关动作
class SC:
    def __init__(self):
        self.State = SC_STATE()

    # 根据最佳路径从而知道下一步怎么走
    def takeAction(self, playerState):
        # 根据当前蝎子和玩家的坐标得到最佳路径（包含当前坐标）
        self.final = bestRouteGenerator(self.State.state, playerState)
        # 总步数在2步以上的话往后选一步
        if len(self.final) >= 2:
            return SC_STATE(self.final[1])
        # 总步数如果只有1，则选这一步
        else:
            return SC_STATE(self.final[-1])

    #将蝎子放回原位
    def reset(self):
        self.State = SC_STATE()

    def play(self, playerState, mummyState, crashCount):
        #蝎子和木乃伊没有相撞的情况
        if crashCount == 0:
            self.State = self.takeAction(playerState)
        #蝎子和木乃伊相撞，将蝎子从棋盘上移除，放到(3, 4)
        else:
            self.State = SC_STATE((3,4))

#与玩家坐标相关的变量和函数
class PLAYER_STATE:
    # 初始化状态
    def __init__(self, state = playerStart):
        self.state = state
        self.isEnd = False
        self.isCaught = False

    # 根据当前坐标是否在出口或陷阱 和 是否被敌人抓住判断游戏是否结束
    def SetEnd(self, isCaught):

        # 到达终点，踩到陷阱或者被抓住都视为游戏结束
        if (self.state == win) or (self.state == trap) or isCaught:
            # 若在终点，将终点状态设为True
            self.isEnd = True

    # 根据动作返回下个落脚点的位置
    def nxt_position(self, action):
        # 向下、向右、向上、向左走不通
        if ((action == 'D') and (self.state in hwallD)) or ((action == 'R') and (self.state in vwallR)) or ((action == 'U') and (self.state in hwallU)) or ((action == 'L') and (self.state in vwallL)):
            return self.state

        # 不同动作带来不同的结果
        if action == 'U':
            nxtState = (self.state[0] - 1, self.state[1])

        elif action == 'D':
            nxtState = (self.state[0] + 1, self.state[1])

        elif action == 'L':
            nxtState = (self.state[0], self.state[1] - 1)

        elif action == 'R':
            nxtState = (self.state[0], self.state[1] + 1)

        # 如果为'S'则保持不动
        # else:
        #     nxtState = self.state

        # 下一步是否在合法范围内
        if (nxtState[0] >= 0) and (nxtState[0] <= (BOARD_ROWS - 1)):
            if (nxtState[1] >= 0) and (nxtState[1] <= (BOARD_COLS - 1)):
                return nxtState
        return self.state

    #奖励设置
    def give_reward(self, isCaught):
        if self.state == win:
            print("win")
            return 100
        elif self.state == trap:
            return -1
        elif isCaught == True:
            return -1
class Player:
    def __init__(self):
        #创建玩家的坐标类的对象
        self.State = PLAYER_STATE(playerStart)
        #
        # self.state = self.State.state
        # 动作列表
        self.action_list = ['U', 'D', 'L', 'R'] #这里暂时没有加上保持不动'S'这个选项
        # 初始化步骤列表
        self.steps_list = []
        # 初始化记录动作的列表
        self.actions_list = []
        # exploration的分配
        self.exp_rate = 0.7
        # 学习速率
        self.lr = 0.1
        # 创建奖励表
        self.board_value = {}
        # 创建终止状态
        self.isEnd = self.State.isEnd
        # 初始化被抓状态
        self.isCaught = self.State.isCaught
        # 初始化奖励表
        for i in range(BOARD_ROWS):
            for j in range(BOARD_COLS):
                self.board_value[(i, j)] = 0

        #记录木乃伊和蝎子足迹的两个列表
        self.mummylist = []
        self.sclist = []

        self.onkeyList = []

    # 1.方法一：选择下一步怎么走，返回一个动作
    def chooseAction(self):
        # 初始化action
        action = 'U'
        # 初始化reward
        reward = 0
        # 30%分配给exploration
        rp = np.random.uniform(0, 1)
        if rp <= self.exp_rate:
            # 随机选择下一步
            action = np.random.choice(self.action_list)

        # 否则哪里分高走哪里
        else:
            for a in self.action_list:
                nxt_reward = self.board_value[self.State.nxt_position(a)]
                if nxt_reward >= reward:
                    reward = nxt_reward
                    action = a
        return action

    # 2.方法二：执行下一步，返回一个坐标
    def takeAction(self, action):
        position = self.State.nxt_position(action)
        # 返回一个更新了的对象
        return PLAYER_STATE(state=position)

    # 3.方法三：清零
    def reset(self):
        self.steps_list = []
        self.actions_list = []
        self.State = PLAYER_STATE()
        self.isEnd = self.State.isEnd
        self.isCaught = self.State.isCaught

        self.mummylist = []
        self.sclist = []

        self.onkeyList = []
    def play(self, mummy, sc, tries = 10):
        # 全局变量水平方向墙壁，用于之后进行和栅栏有关的操作
        global hwallU
        global hwallD

        i = 0
        #所有回合的所有步骤都分类存储在这些列表中
        agentList = []
        mummyList = []
        scList = []
        actionsList = []

        crashCount = 0
        # 玩家踩到钥匙上的次数
        onkey = 0
        onkeyList = []
        while i < tries:
            if self.State.isEnd:
                # 与蝎子相撞有关的重置
                crashCount = 0

                # 步数更新
                agentList.append(self.steps_list)
                mummyList.append(self.mummylist)
                scList.append(self.sclist)
                onkeyList.append(self.onkeyList)
                actionsList.append(self.actions_list)

                # print("mummy:"+str(self.mummylist))
                # print("sc:" + str(self.sclist))
                if self.steps_list[-1] == win:
                    print("player:"+str(self.actions_list))
                # 给予reward
                reward = self.State.give_reward(self.isCaught)

                # 对之前每一步分配点数
                for s in reversed(self.steps_list):
                    # 根据上一格对这一格进行赋值
                    reward = self.board_value[s] + \
                             self.lr * (reward - self.board_value[s])
                    self.board_value[s] = round(reward, 3)

                # 清零
                self.reset()
                mummy.reset()
                sc.reset()
                #对踩到钥匙上的次数也清零
                onkey = 0
                i += 1 #只有结束了才会加一
            else:
                #玩家走一步
                # 选择下一步
                action = self.chooseAction()
                self.actions_list.append(action)
                # 将该步骤保存到步骤列表中
                self.steps_list.append(self.State.nxt_position(action))
                # 迈向下一步(更新对象)
                self.State = self.takeAction(action)

                #判断当前位置是否触发了钥匙
                if self.State.state == key:
                    onkey += 1
                #奇数次放下栅栏，偶数次则升起栅栏
                hwallU = [(1, 0), (1, 7), (1, 8), (2, 3), (3, 4), (3, 7), (4, 4), (4, 7), (5, 3), (5, 8), (6, 2),
                          (7, 2), (8, 3), (8, 8), (8, 9), (9, 1), (9, 4), (8, 2)] if (onkey % 2 == 0) else [(1, 0), (1, 7), (1, 8), (2, 3), (3, 4), (3, 7), (4, 4), (4, 7), (5, 3), (5, 8), (6, 2), (7, 2), (8, 3), (8, 8), (8, 9), (9, 1), (9, 4)]
                hwallD = [(0,0), (0,7), (0,8), (1,3), (2,4), (2,7), (3,4), (3,7), (4,3), (4,8), (5,2), (6,2), (7,3), (7,8), (7,9), (8,1), (8,4), (7,2)] if (onkey % 2 == 0) else [(0,0), (0,7), (0,8), (1,3), (2,4), (2,7), (3,4), (3,7), (4,3), (4,8), (5,2), (6,2), (7,3), (7,8), (7,9), (8,1), (8,4), (7,2)]

                #木乃伊走两步
                mummy.play(self.State.state)

                if (sc.takeAction(self.State.state).state == mummy.State.state):
                    crashCount += 1
                #蝎子走一步
                sc.play(self.State.state, mummy.State.state, crashCount)

                #记录木乃伊和蝎子的足迹
                self.mummylist.append(mummy.State.state)
                self.sclist.append(sc.State.state)

                self.onkeyList.append(onkey)

                #判断是否被敌人抓住
                self.isCaught = (self.State.state == mummy.State.state) or (self.State.state == sc.State.state)
                # if self.State.state == mummy.State.state:
                #     print("caught by mummy!")
                # if self.State.state == sc.State.state:
                #     print("caught by scorpion!")

                #标记状态(到终点与否)
                self.State.SetEnd(self.isCaught)
                self.isEnd = self.State.isEnd

        for i in range(len(agentList)):
            agentList[i].insert(0, playerStart)
            mummyList[i].insert(0, mummyStart)
            scList[i].insert(0, scStart)
            onkeyList[i].insert(0,0)
            actionsList[i].insert(0, '')
        # print('agent:' + str(agentList))
        # print('mummy:' + str(mummyList))
        # print('sc:' + str(scList))
        # print('onkey:'+ str(onkeyList))
        # print("action:" + str(actionsList))
        return agentList, mummyList, scList, onkeyList, actionsList

    def showValues(self):
        for i in range(0, BOARD_ROWS):
            print('-' * 35)
            out = ' | '
            for j in range(0, BOARD_COLS):
                out += str(self.board_value[(i, j)]) + ' | '
            print(out)
        print('-' * 35)


# mummy = MUMMY()
# player = Player()
# sc = SC()
# player.play(mummy, sc, 2)
# player.showValues()
