from matplotlib.pyplot import flag
from draw import *
import math
bonus_points,matrix,start,end=readMatrix('maze/maze_map5.txt')



##########################################################
#                 Heuristic Functions                    #
##########################################################
#Euclidean distance
def heuristic1(start,end):
    h=pow((end[0]-start[0]),2)+pow((end[1]-start[1]),2)
    return math.sqrt(h);

#Manhattan distance
def heuristic2(start,end):
    h=abs(end[0]-start[0]) +  abs(end[1]-start[1])
    return h;
#
def heuristic3(start,end):
    dx = abs(start[0] - end[0])
    dy = abs(start[1] - end[1])
    return  (dx + dy) + (1 - 2 * 1) * min(dx, dy)


def parseRoute(path):
    route=[]
    route.append(path[0])
    for i in path:
        j=route[0]
        if (abs(i[0]-j[0]) + abs(i[1]-j[1])==1):
            route.insert(0,i)
    return route


##########################################################
#               Breadth First Search                     #
##########################################################
def BFS(matrix,start,end):
    queue =[start]
    visited=[]
    path=[]

    while queue:
        node=(x1,y1)=queue.pop(0)
        path.insert(0,node)
        if node==end:
            break
        # Tạo ra 4 hướng
        direction= [ (x1+i,y1+j) for (i,j) in [(-1,0),(0,1),(0,-1),(1,0)] ]  #(-1,0): up, (0,-1):left, #(1,0): down, (0,1):rigth
        # Kiểm tra hướng đi hợp lệ
        for next in direction:
            (x2,y2)=next
            if (next not in  visited) and( matrix[x2][y2]!='x'): 
                queue.append(next)
                visited.append(next)
    # Phân tích đường đi
    route=parseRoute(path)
    return route,visited


##########################################################
#                   Depth First Search                   #
##########################################################
def DFS(matrix,start,end):
    visited=[] #format: [nodo1,node2,...]
    stack= [start] 
    while stack:
        node=(x1,y1) = stack[-1]

        if node not in visited:
            visited.append(node)
        
        if(node ==end):
            break
        check = True
        # Tạo ra 4 hướng
        direction= [ (x1+i,y1+j) for (i,j) in [(-1,0),(0,1),(0,-1),(1,0)] ]
        
        for next in direction:
            (x2,y2)=next
            if (next not in visited) and matrix[x2][y2]!='x':
                stack.append(next)
                check = False
                break
        if check:
            stack.pop(-1)

    return stack,visited





##########################################################
#               Dreedy Best First Search                 #
##########################################################
def GREEDY_BFS(matrix,start,end,heuristic): 
    queuePriority =[[start,heuristic(start,end)]]#Open, Format: [ [node,fx],..] vs fx is heuristic
    visited=[]
    Close=[] #close
    while queuePriority:
        #sắp xếp hàng đợi ưu tiên theo heuristic từ thấp đến cao
        queuePriority.sort(key=lambda x: x[1])
        node,fx=queuePriority.pop(0)
        Close.insert(0,node)
        # Kiểm tra kết thúc
        if(node==end):
            break
        # tạo 4 hướng 
        (x1,y1)=node
        direction= [ (x1+i,y1+j) for (i,j) in [(-1,0),(0,1),(0,-1),(1,0)] ]  #(-1,0): up, (0,-1):left, #(1,0): down, (0,1):rigth
        # Kiểm tra hướng đi hợp lệ và thêm vào queue
        for next in direction:
            hx=heuristic(next,end)  #hàm heuristic  fx=hx
            (x2,y2)=next
            if (next not in visited) and( matrix[x2][y2]!='x'): 
                queuePriority.append([next,hx])
                visited.append(next)
    # Phân tích đường đi
    route=parseRoute(Close)
    return route,visited


##########################################################
#                         A_Star                         #
##########################################################
def A_Star(matrix,start,end,heuristic):
    queuePriority =[[start,0,heuristic2(start,end)]]#Open, Format: [ [node,cost,fx],..] vs fx is heuristic
    Closed=[] #close
    visited = [] #lưu lại các vị trí đã đi
    while queuePriority:
        #sắp xếp hàng đợi ưu tiên theo heuristic từ thấp đến cao
        queuePriority.sort(key=lambda x: x[2])  
        node,cost,fxNode=queuePriority.pop(0)
        Closed.insert(0,node)

        # Kiểm tra kết thúc
        if(node==end):
            break
        # tạo 4 hướng 
        (x1,y1)=node
        direction= [ (x1+i,y1+j) for (i,j)in [(-1,0),(0,1),(0,-1),(1,0)] ]  #(-1,0): up, (0,-1):left, #(1,0): down, (0,1):rigth

        for next in direction:
            (x2,y2)=next
            if (next  not in Closed) and ( matrix[x2][y2]!='x'):
                hx=heuristic(next,end)
                gx=cost+1
                fx= hx+gx
                #Kiểm tra xem next có tồn tại trong openlist (queuePriority):
                    #nếu phải thì kiểm tra xem next.gx có lớn hơn gx của open list
                        #nếu phải thì chuyển hướng khác. nếu ko thì đẩy hướng đó vào openlist
                check=True
                for (open,g,f) in  queuePriority:
                    if next ==open:
                        if fx >=f: 
                            check=False
                if not check: 
                    continue

                queuePriority.append([next,gx,fx])
                visited.append(next)

    # Phân tích đường đi
    route=parseRoute(Closed)
    # route.re
    return route,visited



def A_StarForBonus(matrix,start,end,bonus_points,heuristic):

    bonusPoints=[ [ (x,y),bonus ]  for (x,y,bonus) in bonus_points]
    queuePriority =[[start,0,heuristic(start,end)], ]#Open, Format: [ [node,cost,fx],..] vs fx is heuristic

    route=[] #đường đi
    Closed=[] #close
    visited = [] #lưu lại các vị trí đã đi
    
    #Các mục tiêu cần di chuyển, end và các bonus point
    Goal=[end]
    for (point,bonus) in  bonusPoints: 
        Goal.append(point)

    # Goal
    while queuePriority:
        #sắp xếp hàng đợi ưu tiên theo fx từ thấp đến cao
        queuePriority.sort(key=lambda x: x[2])  
        node,cost,fxNode=queuePriority.pop(0)
        Closed.insert(0,node)

        #kiểm tra node có phải là goal 
        if(node in Goal):
            bonusPoints =[  [point,bunus]  for (point,bunus) in bonusPoints if point!=node ] #remove bonus points
            Goal.remove(node)
            route =Closed.copy() + route
            # route+=parseRoute(Closed)
            queuePriority.clear()
            Closed.clear()
            if node ==end:
                break
         
        # tạo 4 hướng 
        (x1,y1)=node
        direction= [ (x1+i,y1+j) for (i,j)in [(-1,0),(0,1),(0,-1),(1,0)] ]  #(-1,0): up, (0,-1):left, #(1,0): down, (0,1):rigth

        for next in direction:
            (x2,y2)=next
            if (next  not in Closed) and ( matrix[x2][y2]!='x'):

                hx=[heuristic(next,end)]
                for (point,c) in   bonusPoints: 
                    hx.append( heuristic(next,point)+c +heuristic(point,end))
                minhx=min(hx)
                
                for (point,c) in   bonusPoints: 
                    if(next ==point):
                        cost +=c
                        break
                    
                gx=cost+1
                fx= minhx+gx
                #Kiểm tra xem next có tồn tại trong openlist (queuePriority):
                    #nếu phải thì kiểm tra xem next.fx có lớn hơn fx của open list
                        #nếu phải thì chuyển hướng khác. nếu ko thì đẩy hướng đó vào openlist
                check=True
                for (open,g,f) in  queuePriority:
                    if next ==open:
                        if fx >=f: 
                            check=False
                if not check: 
                    continue

                queuePriority.append([next,gx,fx])
                visited.append(next)

    return parseRoute( route),visited

visualize_maze(matrix,bonus_points,start,end)

route,visited=A_StarForBonus(matrix,start,end,bonus_points,heuristic2)
visualize_maze(matrix,bonus_points,start,end,route,visited)



def A_StarForTeleport(matrix,start,end,Gate_points,heuristic):
    #tập hơn các cặp cổng
    GatePoints =[   [(x1,y1),(x2,y2) ] for (x1,y1,k1) in Gate_points  for (x2,y2,k2) in Gate_points if (k1==k2 and x1!=x2 and y1!=y2) ]
    
    queuePriority =[[start,0,heuristic(start,end)], ]#Open, Format: [ [node,cost,fx],..] vs fx is heuristic
    route=[] #đường đi
    Closed=[] #close
    visited = [] #lưu lại các vị trí đã đi
    #Các mục tiêu cần di chuyển, end và cổng dịch chuyển
    Goal=[end]
    for (x,y,k) in  Gate_points: 
        Goal.append((x,y))

    # Goal
    while queuePriority:
        #sắp xếp hàng đợi ưu tiên theo fx từ thấp đến cao
        queuePriority.sort(key=lambda x: x[2])  

        # i=0
        # node,cost,fxNode=queuePriority[0]
        # for   gate1,gate2 in GatePoints:
        #     if node==gate1 or node==gate2:
        #         if node not in Goal:
        #             i+=1
        #     else:
        #         break
        
        node,cost,fxNode=queuePriority.pop(0)

        Closed.insert(0,node)
        print(node)
        #kiểm tra node có phải là goal 
        if(node in Goal ):
        
            route+=parseRoute(Closed)
            if node ==end:
                break

            #tìm 2 công nôi với nhau
            gate1=node
            gate2=None
            for (point1,point2) in GatePoints:
                if(gate1==point1):
                    gate2=point2;
            
            #xóa cổng và chạy lại
            GatePoints.remove([gate1,gate2])
            GatePoints.remove([gate2,gate1])
            Goal.remove(gate1)
            Goal.remove(gate2)
            queuePriority.clear()
            # Closed.clear()
            node=gate2
         
        # tạo 4 hướng 
        (x1,y1)=node
        direction= [ (x1+i,y1+j) for (i,j)in [(-1,0),(0,1),(0,-1),(1,0)] ]  #(-1,0): up, (0,-1):left, #(1,0): down, (0,1):rigth

        for next in direction:
            (x2,y2)=next
            if (next  not in Closed) and ( matrix[x2][y2]!='x') :

                hx=[heuristic(next,end)]
                #tìm cổng dịch chuyển gần nhất và tính heuristic từ next đến cổng đó và cổng đó đến cổng kế tiếp
                for  (gate1,gate2) in GatePoints:
                    hx.append( heuristic(next,gate1)+heuristic(gate2,end))
    
                minhx=min(hx)
                # thêm cặp cổng thoa mã điều kiện vào mục tiêu cần thực
                # for  (gate1,gate2) in GatePoints:
                #     h=heuristic(next,gate1)+heuristic(gate2,end)
                #     if (h<=minhx and gate1 not in Goal ):
                #         Goal.append(gate1)
                #         Goal.append(gate2)


         
                gx=cost+1
                fx= minhx+gx
     
                #Kiểm tra xem next có tồn tại trong openlist (queuePriority):
                    #nếu phải thì kiểm tra xem next.fx có lớn hơn fx của open list
                        #nếu phải thì chuyển hướng khác. nếu ko thì đẩy hướng đó vào openlist
                check=True
                for (open,g,f) in  queuePriority:
                    if next ==open:
                        if fx >=f: 
                            check=False
                if not check: 
                    continue

                queuePriority.append([next,gx,fx])
                visited.append(next)

    return route,visited



# route,visited=A_StarForTeleport(matrix,start,end,bonus_points,heuristic1)
# visualize_maze(matrix,bonus_points,start,end,route,visited)

# route,visited=DFS(matrix,start,end)
# visualize_maze(matrix,bonus_points,start,end,route,visited)

# route,visited=GREEDY_BFS(matrix,start,end,heuristic3)
# visualize_maze(matrix,bonus_points,start,end,route,visited)

# route,visited=A_Star(matrix,start,end,heuristic3)
# visualize_maze(matrix,bonus_points,start,end,route,visited)







# A* Search Algorithm
# let openList equal empty list of nodes
# let closedList equal empty list of nodes
# put startNode on the openList (leave it's f at zero)
# while openList is not empty
#     let currentNode equal the node with the least f value
#     remove currentNode from the openList
#     add currentNode to the closedList
#     if currentNode is the goal
#         You've found the exit!
#     let children of the currentNode equal the adjacent nodes
#     for each child in the children
#         if child is in the closedList
#             continue to beginning of for loop
#         child.g = currentNode.g + distance b/w child and current
#         child.h = distance from child to end
#         child.f = child.g + child.h
#         if child.position is in the openList's nodes positions
#             if child.g is higher than the openList node's g
#                 continue to beginning of for loop
#         add the child to the openList



# // A* Search Algorithm
# 1.  Initialize the open list
# 2.  Initialize the closed list
#     put the starting node on the open 
#     list (you can leave its f at zero)

# 3.  while the open list is not empty
#     a) find the node with the least f on 
#        the open list, call it "q"

#     b) pop q off the open list
  
#     c) generate q's 8 successors and set their 
#        parents to q
   
#     d) for each successor
#         i) if successor is the goal, stop search
#           successor.g = q.g + distance between 
#                               successor and q
#           successor.h = distance from goal to 
#           successor (This can be done using many 
#           ways, we will discuss three heuristics- 
#           Manhattan, Diagonal and Euclidean 
#           Heuristics)
          
#           successor.f = successor.g + successor.h
#         ii) if a node with the same position as 
#             successor is in the OPEN list which has a 
#            lower f than successor, skip this successor

#         iii) if a node with the same position as 
#             successor  is in the CLOSED list which has
#             a lower f than successor, skip this successor
#             otherwise, add  the node to the open list
#      end (for loop)
  
#     e) push q on the closed list
#     end (while loop)