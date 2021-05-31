from queue import Queue

class Vertex:
    def __init__(self,id:int):
        self.id = id
        self.adj_list = []
        self.visited = False
        self.path = float("inf")
        self.prev = self
        self.prev_w = 0

    def add(self,vertex,weight:float):
        self.adj_list.append((vertex,weight))

    def __str__(self):
        ret = "["
        if len(self.adj_list)==0:
            return "[]"
        for i in self.adj_list[:-1]:
            ret += f"({i[0].id}:{i[1]}),"
        ret += f"({self.adj_list[-1][0].id}:{self.adj_list[-1][1]})]"
        return ret


def read_from_file(path):
    f = open(path,"r")
    text = f.read()
    f.close()

    i = text.find("[")+1
    l_list = []
    while i<len(text) and i>0:
        i = text.find("[",i)+1
        if i==0: break
        l_list.append(text[i:text.find("]",i)])
        i = text.find("]",i)+1
    v_list = []
    for i in range(len(l_list)):
        v_list.append(Vertex(i))
    for i in range(len(l_list)):
        for e in l_list[i].split(","):
            e = e[e.find("(")+1:e.find(")")]
            vertex = v_list[int(e.split(":")[0])]
            weight = float(e.split(":")[1])
            v_list[i].add(vertex,weight)

    return v_list


def write_to_file(path,v_list):
    try:
        f = open(path,"w")
    except FileNotFoundError:
        print(f"File {path} does not exist!")
        return
    f.write("[")
    for v in v_list[:-1]:
        f.write(str(v)+",\n")
    f.write(str(v)+"]")
    f.close()


def dijkstra(start:Vertex):
    q = Queue()
    start.path = 0
    q.put(start)
    while not q.empty():
        v = q.get()
        if v.visited: continue
        for i in v.adj_list:
            if not i[0].visited and v.path+i[1]<i[0].path:
                i[0].path = v.path+i[1]
                i[0].prev = v
                i[0].prev_w = i[1]
                q.put(i[0])
        v.visited = True


while True:
    name = input("Podaj nazwę pliku do odczytu:")
    try:
        vertices = read_from_file(name)
        break
    except FileNotFoundError:
        print("Podany plik nie istnieje!")

while True:
    n = input(f"Podaj węzeł początkowy (0-{len(vertices)-1}):")
    try:
        n = int(n)
        if n>=0 and n<len(vertices):
            break
        print("Nieprawidłowy węzeł")
    except ValueError:
        print("Nieprawidłowy węzeł")

dijkstra(vertices[n])
t_list = []
for i in range(len(vertices)):
    t_list.append(Vertex(i))
for v in vertices:
    if v.id != v.prev.id:
        t_list[v.prev.id].add(v,v.prev_w)
write_to_file("dji_tree.txt",t_list)