# 显示游戏窗口
# 坦克大战小游戏需求分析：
# 坦克类：我方坦克类、敌方坦克类、坦克的显示、移动、射击
# 子弹类：显示子弹、子弹的移动
# 墙壁类：显示墙壁
# 爆炸效果类：显示爆炸效果
# 音效类：播放音效
# 游戏主类：开始游戏、结束游戏
# 写代码时可能还需要在这些类中添加其他对应的方法，因此具体情况将具体分析

import pygame
import time
import random
import sys

# 设置通用属性
WINDOWS_COLOR = pygame.Color(0,0,0)   # 设置窗口填充颜色
TEXT_COLOR = pygame.Color(255,0,0)      # 设置字体颜色
SCREEN_WIDTH = 700      # 设置窗口宽度
SCREEN_HEIGHT = 500     # 设置窗口高度

class MainGame():
    '''游戏主类'''
    window = None   # 创建一个表示窗口的类属性对象
    my_tank = None  # 创建一个我方坦克的类属性对象
    # enemy_tank_count = 6    # 设置敌方坦克的默认数量，创建一个类属性对象
    enemy_tank_count = 4    # 设置敌方坦克的默认数量，创建一个类属性对象
    enemy_tank_list = []     # 创建存储敌方坦克的列表的类属性对象
    my_bullet_list = []      # 创建存储我方坦克子弹的列表的类属性对象
    enemy_bullet_list = []   # 创建存储敌方坦克子弹的列表的类属性对象
    explode_list = []       # 创建一个存储爆炸效果的列表对的类属性对象
    wall_list = []          # 创建一个墙壁的列表对的类属性对象

    def __init__(self) ->  None:
        '''游戏主类的构造方法'''
        pass

    def start_game(self):
        '''开始游戏'''
        # 初始函数，使用pygame的第一步（初始化游戏窗口）
        pygame.display.init()
        # 创建一个窗口
        MainGame.window = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        # 设置窗口标题
        pygame.display.set_caption("坦克大战1.0")
        # 创建一个我方坦克
        self.creat_my_tank()
        # 播放开始游戏音效
        music = Music('./img/start.wav')
        music.display_music()
        # 创建敌方坦克
        self.creat_enemy_tank()
        # 创建墙壁
        self.creat_wall()

        # 刷新窗口
        while True:
            time.sleep(0.02)    # 延迟刷新0.02秒
            MainGame.window.fill(WINDOWS_COLOR)     # 填充窗口颜色
            # 要增加的文字内容
            text01 = self.get_text_surface(f"敌方剩余坦克数量为：{len(MainGame.enemy_tank_list)}")
            # 判断我方坦克是否活着且不为空
            if MainGame.my_tank and MainGame.my_tank.live:
                # 要增加的文字内容
                text02 = self.get_text_surface(f"我方坦克剩余生命值为：{MainGame.my_tank.hp}")
            else:
                # 要增加的文字内容
                text02 = self.get_text_surface("我方坦克剩余生命值为：0")
            # 如何把文字加上且设置文字显示的坐标位置
            MainGame.window.blit(text01,(10,10))
            MainGame.window.blit(text02,(10,40))
            # 判断我方坦克是否活着且不为空
            if MainGame.my_tank and MainGame.my_tank.live:
                # 显示我方坦克
                MainGame.my_tank.display_tank()
            else:
                # 将类对象my_tank设置为 None 类型的对象
                MainGame.my_tank = None
                print("很遗憾，游戏失败~~")
                self.end_game()        
            # 增加事件
            self.get_event()
            # 显示并随机移动敌方坦克
            self.display_and_move_enemy_tank()
            # 显示和移动我方坦克子弹
            self.display_and_move_my_bullet()
            # 显示和移动敌方坦克子弹
            self.display_and_move_enemy_bullet()
            # 显示爆炸效果
            self.display_explode()
            # 显示墙壁
            self.display_wall()
            # 判断我方坦克是否活着且不为空
            if MainGame.my_tank and MainGame.my_tank.live:
                # 移动我方坦克
                if MainGame.my_tank.remove:     # 如果标志位为True才移动，否则不移动
                    MainGame.my_tank.move_tank()
                    # 检测我方坦克是否与墙壁发生碰撞
                    MainGame.my_tank.tank_hit_wall()
                    # 检测我方坦克是否与敌方坦克发生碰撞
                    for enemy_tank in MainGame.enemy_tank_list:
                        MainGame.my_tank.tank_hit_tank(enemy_tank)
            pygame.display.update()     # 刷新窗口

    def get_text_surface(self,text):
        '''获取字体图片'''
        # 初始化字体模块
        pygame.font.init()
        # 获取可以使用的字体
        # print(pygame.font.get_fonts())    # 运行后发现系统可使用的字体中包含'kaiti'
        # 创建字体
        font = pygame.font.SysFont("kaiti",18)
        # 绘制文字信息
        text_surface = font.render(text,True,TEXT_COLOR)
        # 将绘制的文字信息返回
        return text_surface


    def get_event(self):
        '''获取事件方法 '''
        # 获取所有事件
        event_list = pygame.event.get()
        # 遍历事件
        for event in event_list:
            # 判断是什么事件，然后做出相应的处理
            if event.type == pygame.QUIT:
                self.end_game()      # 如果点击关闭按钮则退出游戏
            # 按下键盘
            if event.type == pygame.KEYDOWN:
                # 判断我方坦克是否活着且不为空
                if MainGame.my_tank and MainGame.my_tank.live:
                    # 判断是否是方向左键按下
                    if event.key == pygame.K_LEFT:
                        print("坦克向左移动")
                        # 修改坦克方向，使得坦克方向向左
                        MainGame.my_tank.direction = "L"
                        # 更改我方坦克移动标志为True
                        MainGame.my_tank.remove = True
                    # 判断是否是方向右键按下
                    elif event.key == pygame.K_RIGHT:
                        print("坦克向右移动")
                        # 修改坦克方向，使得坦克方向向右
                        MainGame.my_tank.direction = "R"
                        # 更改我方坦克移动标志为True
                        MainGame.my_tank.remove = True
                    # 判断是否是方向上键按下
                    elif event.key == pygame.K_UP:
                        print("坦克向上移动")
                        # 修改坦克方向，使得坦克方向向上
                        MainGame.my_tank.direction = "U"
                        # 更改我方坦克移动标志为True
                        MainGame.my_tank.remove = True
                    # 判断是否是方向下键按下
                    elif event.key == pygame.K_DOWN:
                        print("坦克向下移动")
                        # 修改坦克方向，使得坦克方向向下
                        MainGame.my_tank.direction = "D"
                        # 更改我方坦克移动标志为True
                        MainGame.my_tank.remove = True
                    # 判断空格键是否按下
                    elif event.key == pygame.K_SPACE:
                        # 控制子弹的发送数量，避免电脑内存的过度消耗
                        if len(MainGame.my_bullet_list) <= 20:
                            # 我方坦克发射子弹
                            print("发射子弹")
                            # 创建我方坦克子弹
                            my_bullet = Bullet(MainGame.my_tank)
                            # 将子弹添加到列表中
                            MainGame.my_bullet_list.append(my_bullet)
            # 松开键盘且为方向键
            if event.type == pygame.KEYUP and event.key in (pygame.K_RIGHT, pygame.K_LEFT, pygame.K_UP, pygame.K_DOWN):
                # 判断我方坦克是否活着且不为空
                if MainGame.my_tank and MainGame.my_tank.live:
                        # 更改移动标志为False
                        MainGame.my_tank.remove = False

    def creat_enemy_tank(self):
        '''创建敌方坦克方法'''
        # 设置敌方坦克距离上边界的位置
        top = 100
        # 设置敌方坦克的移动速度
        # speed = random.randint(3,5)
        speed = random.randint(1,3)
        # 生成6个敌方坦克
        for i in range(MainGame.enemy_tank_count):
            # 随机设置6个敌方坦克距离左边界的位置
            left = random.randint(0,600)
            # 创建敌方坦克对象
            enemy_tank = EnemyTank(left,top,speed)
            # 将每个敌方坦克对象存在敌方坦克列表中
            MainGame.enemy_tank_list.append(enemy_tank)

    def creat_my_tank(self):
        '''创建我方坦克的方法'''
        # 创建一个我方坦克
        MainGame.my_tank = MyTank(325,225)

    def creat_wall(self):
        '''创建墙壁的方法'''
         # 设置墙壁距离上边界的位置
        top = 150
        # 生成6个墙壁
        for i in range(6):
            # 设置6个墙壁距离左边界的位置
            left = i*128
            # 创建墙壁对象
            wall = Wall(left,top)
            # 将创建的所有墙壁对象添加到存储墙壁的列表当中
            MainGame.wall_list.append(wall)

    def display_and_move_enemy_tank(self):
        '''显示和移动敌方坦克的方法'''
        # 遍历创建敌方坦克的列表成员的对象
        for enemy_tank in MainGame.enemy_tank_list:
            # 判断敌方坦克存活状态，若存活则展示、移动和发射子弹
            if enemy_tank.live:
                enemy_tank.display_tank()   # 展示敌方坦克
                # 移动敌方坦克
                enemy_tank.rand_move()
                # 判断敌方坦克是否与墙壁发生碰撞
                enemy_tank.tank_hit_wall()
                # 判断敌方坦克是否与我方坦克发生碰撞
                enemy_tank.tank_hit_tank(MainGame.my_tank)
                # 敌方坦克发射子弹
                enemy_bullet = enemy_tank.shot()
                # 判断子弹是否存在
                if enemy_bullet:
                    # 将子弹添加到敌方存储子弹的列表中
                    MainGame.enemy_bullet_list.append(enemy_bullet)
            # 否则将敌方坦克移除存储敌方坦克的列表
            else:
                # 将淘汰的敌方坦克移除存储敌方坦克的列表
                MainGame.enemy_tank_list.remove(enemy_tank)
        # 判断敌方坦克是否全部死亡
            if len(MainGame.enemy_tank_list) == 0:
                print("游戏胜利，恭喜你成功保卫了家园！！！")
                self.end_game()      # 如果敌方坦克全部死亡则游戏结束

    def display_and_move_enemy_bullet(self):
        '''显示和移动的敌方坦克的子弹'''
        # 遍历创建敌方坦克的子弹列表成员的对象
        for enemy_bullet in MainGame.enemy_bullet_list:
            # 判断敌方坦克的子弹存活状态，存活则展示和移动，消亡则从子弹列表中移除
            if enemy_bullet.live:
                enemy_bullet.display_bullet()   # 展示敌方坦克子弹
                enemy_bullet.move_bullet()      # 移动敌方坦克子弹
                enemy_bullet.hit_my_tank()      # 判断敌方坦克子弹是否击中我方坦克
                enemy_bullet.hit_wall()         # 判断敌方坦克子弹是否击中墙壁
            else:
                # 将消亡的子弹从子弹列表中移除
                MainGame.enemy_bullet_list.remove(enemy_bullet)

    def display_and_move_my_bullet(self):
        '''显示和移动我方坦克的子弹'''
        # 遍历创建我方坦克的子弹列表成员的对象
        for my_bullet in MainGame.my_bullet_list:
            # 判断我方坦克的子弹存活状态，存活则展示和移动，消亡则从子弹列表中移除
            if my_bullet.live:
                my_bullet.display_bullet()  # 展示我方坦克子弹
                my_bullet.move_bullet()     # 移动我方坦克子弹
                my_bullet.hit_enemy_tank()  # 判断我方坦克子弹是否击中敌方坦克
                my_bullet.hit_wall()        # 判断我方坦克子弹是否击中墙壁
            else:
                # 将消亡的子弹从子弹列表中移除
                MainGame.my_bullet_list.remove(my_bullet)

    def display_explode(self):
        '''显示爆炸效果的方法'''
        for explorde in MainGame.explode_list:
            # 判断爆炸是否存活，存活则显示爆炸效果和音效，消亡则从爆炸列表中移除
            if explorde.live:
                explorde.display_explode()      # 显示爆炸效果
                # 显示爆炸音效
                music = Music('./img/fire.wav')     # 导入音效文件
                music.display_music()               # 播放爆炸音效
            else:
                # 将消亡的爆炸从爆炸列表中移除
                MainGame.explode_list.remove(explorde)

    def display_wall(self):
        '''显示墙壁的方法'''
        for wall in MainGame.wall_list:
            # 判断墙壁是否存活，存活则显示墙壁，消亡则从墙壁列表中移除
            if wall.live:
                wall.display_wall()     # 显示墙壁
            else:
                # 将消亡的墙壁从墙壁列表中移除
                MainGame.wall_list.remove(wall)

    def end_game(self):
        '''结束游戏'''
        print("游戏结束，期待你的下次表现")
        pygame.display.quit()       # 关闭游戏窗口但不退出程序
        # input("请输入回车键退出程序")  # 保持可执行文件窗口不动，按下回车键后才退出
        sys.exit()  # 调用操作系统模块的退出程序函数，使用前要导入sys模块

class Tank():
    '''坦克类'''
    def __init__(self):
        '''坦克类的构造方法'''
        # 设置坦克的存活状态
        self.live = True    # 默认坦克存活
        # 记录坦克原来的位置
        self.old_left = 0
        self.old_top = 0

    def move_tank(self):
        '''坦克的移动方法'''
        # 记录坦克原来的位置，方便还原碰撞后的位置
        self.old_left = self.rect.left
        self.old_top = self.rect.top
        # 判断坦克的位置朝向，位置朝向向左则向左移动
        if self.direction == 'L':
            # 判断坦克是否到达左边界，未到达则可以向左移动
            if self.rect.left > 0:
                # 修改坦克的位置：离左边的距离    - 操作
                self.rect.left -= self.speed
        # 判断坦克的位置朝向，位置朝向向右则向右移动
        elif self.direction == 'R':
            # 判断坦克是否到达右边界，未到达则可以向右移动
            if self.rect.left + self.rect.width < SCREEN_WIDTH:
                # 修改坦克的位置：离左边的距离    + 操作
                self.rect.left += self.speed
        # 判断坦克的位置朝向，位置朝向向上则向上移动
        elif self.direction == 'U':
            # 判断坦克是否到达上边界，未到达则可以向上移动
            if self.rect.top > 0:
                # 修改坦克的位置：离上边的距离    - 操作
                self.rect.top -= self.speed
        # 判断坦克的位置朝向，位置朝向向下则向下移动
        elif self.direction == 'D':
            # 判断坦克是否到达下边界，未到达则可以向下移动
            if self.rect.top + self.rect.height < SCREEN_HEIGHT:
                # 修改坦克的位置：离下边的距离    - 操作
                self.rect.top += self.speed

    def tank_hit_wall(self):
        '''检测坦克碰撞墙壁的方法'''
        for wall in MainGame.wall_list:
            # 判断坦克是否撞墙
            if pygame.sprite.collide_rect(self,wall):
                # 将位置还原到碰撞前的位置
                self.rect.left = self.old_left
                self.rect.top = self.old_top


    def tank_hit_tank(self,tank):
        '''检测2个坦克是否发生碰撞'''
        # 判断双方坦克状态是否都存活
        if self.live and tank:
            # 判断双方坦克是否发生碰撞
            if pygame.sprite.collide_rect(self,tank):
                # 将位置还原为碰撞前的位置
                self.rect.left = self.old_left
                self.rect.top = self.old_top

    def display_tank(self) :
        '''展示坦克的方法'''
        # 获取最新坦克的朝向位置图片
        self.image = self.images.get(self.direction)
        # 将坦克图片渲染在窗口中
        MainGame.window.blit(self.image,self.rect)

    def shot(self) -> None:
        '''坦克的射击方法'''
        pass


class MyTank(Tank):
    '''我方坦克类'''
    def __init__(self, left, top):
        '''我方坦克类构造方法'''
        # 继承坦克类（父类）的构造方法
        super(MyTank,self).__init__()
        # 设置我方坦克图片资源
        self.images = {
            'U': pygame.image.load("./img/p1tankU.gif"),  # 我方坦克朝向向上的图片
            'D': pygame.image.load("./img/p1tankD.gif"),  # 我方坦克朝向向下的图片
            'R': pygame.image.load("./img/p1tankR.gif"),  # 我方坦克朝向向右的图片
            'L': pygame.image.load("./img/p1tankL.gif"),  # 我方坦克朝向向左的图片
        }
        # 设置我方坦克的方向
        self.direction = "U"
        # 获取图片信息
        self.image = self.images.get(self.direction)
        # 获取图片的矩形
        self.rect = self.image.get_rect()
        # 设置我方坦克位置
        self.rect.left = left
        self.rect.top = top
        # 设置我方坦克移动速度
        self.speed = 10
        # 设置我方坦克移动标志
        self.remove = False
        # 设置我方坦克的额生命值
        # self.hp = 5
        self.hp = 15

    def tank_hit_wall(self):
        '''检测坦克碰撞墙壁的方法'''
        for wall in MainGame.wall_list:
            # 判断坦克是否撞墙
            if pygame.sprite.collide_rect(self,wall):
                # 将位置还原到碰撞前的位置
                self.rect.left = self.old_left
                self.rect.top = self.old_top
                # 播放撞墙音效
                music = Music('./img/hit.wav')
                music.display_music()


class EnemyTank(Tank):
    '''敌方坦克类'''
    def __init__(self,left,top,speed) :
        '''敌方坦克类的构造方法'''
        # 继承坦克类（父类）的构造方法
        super(EnemyTank,self).__init__()
        # 设置敌方坦克图片资源
        self.images = {
            'U':pygame.image.load('./img/enemy1U.gif'),
            'D':pygame.image.load('./img/enemy1D.gif'),
            'L':pygame.image.load('./img/enemy1L.gif'),
            'R':pygame.image.load('./img/enemy1R.gif')
        }
        # 设置敌方坦克的方向
        self.direction = self.rand_direction()
        # 获取图片信息
        self.image = self.images.get(self.direction)
        # 获取图片的矩形
        self.rect = self.image.get_rect()
        # 设置敌方坦克位置
        self.rect.left = left
        self.rect.top = top
        # 设置敌方坦克移动速度
        self.speed = speed
        # 设置敌方坦克移动标志
        self.remove = False
        # 设置敌方坦克移动的步长
        self.step = 20

    def rand_direction(self):
        '''随机选取敌方坦克朝向的方法'''
        num = random.randint(1,4)
        # 如果生成的随机数为 1 则返回位置朝向为上的图片
        if num == 1:
            return "U"
        # 如果生成的随机数为 2 则返回位置朝向为下的图片
        elif num == 2:
            return "D"
        # 如果生成的随机数为 3 则返回位置朝向为左的图片
        elif num == 3:
            return "L"
        # 如果生成的随机数为 4 则返回位置朝向为右的图片
        elif num == 4:
            return "R"

    def rand_move(self):
        '''随机移动敌方坦克的方法'''
        # 如果敌方坦克的剩余步长小于等于0则随机变换方向
        if self.step <= 0:
            self.direction = self.rand_direction()
            self.step = 20      # 变换方向完则重置步长防止坦克原地转圈圈
        else:
            self.move_tank()    # 步长大于0则移动敌方坦克
            self.step -= 1      # 移动步长逐渐减少

    def shot(self):
        # 设置敌方坦克发射子弹的频率
        num = random.randint(1,100)

        # if num <= 5:        # 如果随机数生成的数字小于等于 5 则返回Bullet()的类对象
        #     return Bullet(self)
        
        if num <= 2:        # 如果随机数生成的数字小于等于 2 则返回Bullet()的类对象
            return Bullet(self)


class Bullet():
    '''子弹类'''
    def __init__(self,tank):
        '''子弹类的构造方法'''
        # 加载子弹图片
        self.image = pygame.image.load("./img/enemymissile.gif")
        # 获取子弹方向
        self.direction = tank.direction
        # 获取子弹的矩形
        self.rect = self.image.get_rect()
        # 设置子弹的位置，先判断子弹方向，然后通过计算设置子弹位置，使子弹出现在炮口上
        if self.direction == 'L':
            self.rect.left = tank.rect.left - self.rect.width
            self.rect.top = tank.rect.top + tank.rect.height/2 - self.rect.height/2
        elif self.direction == 'R':
            self.rect.left = tank.rect.left + tank.rect.width
            self.rect.top = tank.rect.top + tank.rect.height/2 - self.rect.height/2
        elif self.direction == 'U':
            self.rect.left = tank.rect.left + tank.rect.width/2 - self.rect.width/2
            self.rect.top = tank.rect.top - self.rect.height
        elif self.direction == 'D':
            self.rect.left = tank.rect.left + tank.rect.width/2 - self.rect.width/2
            self.rect.top = tank.rect.top + tank.rect.height
        # 设置子弹的速度
        self.speed = 10
        # 设置子弹的存活状态
        self.live = True    # 默认子弹存活

    def display_bullet(self):
        '''展示子弹的方法'''
        # 将子弹图片渲染在窗口中
        MainGame.window.blit(self.image,self.rect)

    def move_bullet(self):
        '''子弹移动的方法'''
        # 判断子弹的位置朝向，位置朝向向左则向左移动
        if self.direction == 'L':
            # 判断子弹是否到达左边界，未到达则可以向左移动，到达则消亡
            if self.rect.left > 0:
                # 修改子弹的位置：离左边的距离    - 操作
                self.rect.left -= self.speed
            else:
                # 更改子弹存活状态为消亡
                self.live = False
        # 判断子弹的位置朝向，位置朝向向右则向右移动
        elif self.direction == 'R':
            # 判断子弹是否到达右边界，未到达则可以向右移动，到达则消亡
            if self.rect.left + self.rect.width < SCREEN_WIDTH:
                # 修改子弹的位置：离右边的距离    + 操作
                self.rect.left += self.speed
            else:
                # 更改子弹存活状态为消亡
                self.live = False
        # 判断子弹的位置朝向，位置朝向向上则向上移动
        elif self.direction == 'U':
            # 判断子弹是否到达上边界，未到达则可以向上移动，到达则消亡
            if self.rect.top > 0:
                # 修改子弹的位置：离上边的距离    - 操作
                self.rect.top -= self.speed
            else:
                # 更改子弹存活状态为消亡
                self.live = False
        # 判断子弹的位置朝向，位置朝向向下则向下移动
        elif self.direction == 'D':
            # 判断子弹是否到达下边界，未到达则可以向下移动，到达则消亡
            if self.rect.top + self.rect.height < SCREEN_HEIGHT:
                # 修改子弹的位置：离下边的距离    + 操作
                self.rect.top += self.speed
            else:
                # 更改子弹存活状态为消亡
                self.live = False

    def hit_my_tank(self):
        '''检测敌方子弹碰撞我方坦克的方法'''
        # 判断我方坦克的存活状态并且是否为空
        if MainGame.my_tank and MainGame.my_tank.live:
            # 判断我方坦克与敌方子弹是否发生碰撞
            if pygame.sprite.collide_rect(self,MainGame.my_tank):
                # 创建爆炸效果的类对象
                explode = Explode(MainGame.my_tank)
                # 将爆炸效果添加到存储爆炸效果的列表当中
                MainGame.explode_list.append(explode)
                # 敌方子弹更改存活状态为消亡状态
                self.live = False
                # 我方坦克生命值-1
                MainGame.my_tank.hp -= 1
                # 判断我方坦克的生命值是否小于等于0，如果是则我方坦克更改存活状态为消亡状态
                if MainGame.my_tank.hp <= 0:
                    # 我方坦克更改存活状态为消亡状态
                    MainGame.my_tank.live = False
                

    def hit_enemy_tank(self):
        '''检测我方子弹碰撞敌方坦克的方法'''
        # 遍历创建敌方坦克的列表成员的对象
        for enemy_tank in MainGame.enemy_tank_list:
            # 如果敌方坦克和我方子弹碰撞，则我方子弹和敌方坦克更改存活状态为消亡状态
            if pygame.sprite.collide_rect(self,enemy_tank):
                # 爆炸效果
                explode = Explode(enemy_tank)
                # 将爆炸效果添加到存储爆炸效果的列表当中
                MainGame.explode_list.append(explode)
                # 敌方坦克更改存活状态为消亡状态
                enemy_tank.live = False
                # 我方子弹更改存活状态为消亡状态
                self.live = False

    def hit_wall(self):
        '''检测子弹碰撞墙壁的方法'''
        # 遍历创建墙壁的列表成员的对象
        for wall in MainGame.wall_list:
            # 如果子弹与墙壁碰撞，则子弹更改存活状态为消亡状态
            if pygame.sprite.collide_rect(self,wall):
                # 子弹更改存活状态为消亡状态
                self.live = False
                # 修改墙壁的生命值
                wall.hp -= 1
                # 判断墙壁是否依然显示
                if wall.hp <= 0:
                    wall.live = False


class Wall():
    '''墙壁类'''
    def __init__(self,left,top):
        '''墙壁类的构造方法'''
        # 加载墙壁图片
        self.image = pygame.image.load('./img/steels.gif')
        # 获取墙壁的图形
        self.rect = self.image.get_rect()
        # 设置墙壁的位置
        self.rect.left = left
        self.rect.top = top
        # 设置墙壁的生命
        self.hp = 3
        # 设置墙壁的存活状态
        self.live = True

    def display_wall(self):
        '''展示墙壁类的方法'''
        # 将墙壁图片渲染在窗口中
        MainGame.window.blit(self.image,self.rect)


class Explode():
    '''爆炸效果类'''
    def __init__(self,tank)-> None:
        '''爆炸效果类的构造方法'''
        # 加载爆炸效果的图片
        self.images = [
            pygame.image.load("./img/blast0.gif"),
            pygame.image.load('./img/blast1.gif'),
            pygame.image.load('./img/blast2.gif'),
            pygame.image.load('./img/blast3.gif')
        ]
        # 设置爆炸效果的位置
        self.rect = tank.rect
        # 设置爆炸效果的索引
        self.step = 0
        # 获取图片信息
        self.image = self.images[self.step]
        # 设置爆炸的状态
        self.live = True

    def display_explode(self):
        '''展示爆炸效果类的方法'''
        # 判断当前爆照的额效果是否播放完毕：
        if self.step < len(self.images):
            # 获取当前爆炸效果的图像
            self.image = self.images[self.step]
            # 获取下一张爆炸效果的图像的索引
            self.step += 1
            # 绘制爆炸效果
            MainGame.window.blit(self.image,self.rect)
        else:
            # 初始化爆炸效果索引
            self.step = 0
            # 设置爆炸效果的状态，代表爆炸过了
            self.live = False


class Music():
    '''音效类'''
    def __init__(self,filename) -> None:
        '''音效类的构造方法'''
        # 创建一个表示文件名的实例属性
        self.filename = filename
        # 初始化混合器
        pygame.mixer.init()
        # 加载音乐文件
        pygame.mixer.music.load(filename)

    def display_music(self)-> None:
        '''展示音效类的方法'''
        # 播放音效
        pygame.mixer.music.play()


if __name__ == '__main__':
    MainGame().start_game()