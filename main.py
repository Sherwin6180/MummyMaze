from MazeDrawer import *
from MummyMaze_QLearning import *
from png2gif import *
import ffmpy

turns = 100
mummy = MUMMY()
player = Player()
sc = SC()
agentList, mummyList, scList, onkeyList, actionsList = player.play(mummy, sc, turns)
# print('agent:'+str(agentList))
# print('mummy:'+str(mummyList))
# print('sc:'+str(scList))

step = 1
for i in range(turns):
    for j in range(len(agentList[i])):
        mazeDrawer = MazeDrawer(agentList[i][j][0], agentList[i][j][1],
                                mummyList[i][j][0], mummyList[i][j][1],
                                scList[i][j][0], scList[i][j][1],
                                onkeyList[i][j],
                                i + 1, j,
                                actionsList[i][j])
        mazeDrawer.saveFrame(step)
        step += 1

# graph_average_reward(player.average_reward_for_each_game)

# gifWriter()
#
# ff = ffmpy.FFmpeg(inputs={'movie.gif': None},
#                   outputs={'output.mp4': None})
# ff.run()
