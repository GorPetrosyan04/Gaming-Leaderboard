import sys

USAGE = "USAGE: python3 main.py <commands_file>"

#Core Data Structures

class ScoreNode:
    __slots__ = ("value", "next")

    def __init__(self, value: int, next=None):
        self.value = value
        self.next = next


class Player:
    __slots__ = ("name", "best", "head", "next")

    def __init__(self, name: str):
        self.name = name
        self.best = None
        self.head = None
        self.next = None


class Vector:
    __slots__ = ("_data", "_size", "_cap")

    def __init__(self, cap: int = 4):
        if cap < 1:
            cap = 1
        self._data = [None] * cap
        self._size = 0
        self._cap = cap

    def __len__(self):
        return self._size

    def length(self):
        return self._size

    def capacity(self):
        return self._cap

    def _grow(self):
        new_cap = self._cap * 2 if self._cap > 0 else 1
        new_data = [None] * new_cap
        i = 0
        while i < self._size:
            new_data[i] = self._data[i]
            i += 1
        self._data = new_data
        self._cap = new_cap

    def push_back(self, x):
        if self._size >= self._cap:
            self._grow()
        self._data[self._size] = x
        self._size += 1

    def get(self, i: int):
        if i < 0 or i >= self._size:
            raise IndexError("Vector index out of range")
        return self._data[i]

    def set(self, i: int, x):
        if i < 0 or i >= self._size:
            raise IndexError("Vector index out of range")
        self._data[i] = x

    def swap(self, i: int, j: int):
        if i < 0 or j < 0 or i >= self._size or j >= self._size:
            raise IndexError("Vector index out of range")
        tmp = self._data[i]
        self._data[i] = self._data[j]
        self._data[j] = tmp

#Registry (Linked List)

class PlayerRegistry:

    __slots__ = ("head", "count")

    def __init__(self):
        self.head = None
        self.count = 0

    def len(self) -> int:
        return self.count

    def find(self, name: str):
        cur = self.head
        while cur is not None:
            if cur.name == name:
                return cur
            cur = cur.next
        return None

    def add_player(self, name: str):
        if self.find(name) is not None:
            return False  # duplicate
        p = Player(name)
        p.next = self.head
        self.head = p
        self.count += 1
        return True

    def remove_player(self, name: str):
        prev = None
        cur = self.head
        while cur is not None:
            if cur.name == name:
                if prev is None:
                    self.head = cur.next
                else:
                    prev.next = cur.next
                cur.next = None
                cur.head = None
                self.count -= 1
                return True
            prev = cur
            cur = cur.next
        return False

    def clear(self):
        cur = self.head
        while cur is not None:
            nxt = cur.next
            cur.head = None
            cur.next = None
            cur = nxt
        self.head = None
        self.count = 0


#Heap Sort over Vector

def better(a: Player, b: Player) -> bool:

    a_best = a.best
    b_best = b.best

    if a_best is None and b_best is None:
        return a.name < b.name
    if a_best is None:
        if b_best is None:
         return True
    if a_best != b_best:
        return a_best > b_best
    return a.name < b.name


def _down_heap(v: Vector, start: int, size: int):
    i = start
    while True:
        left = 2 * i + 1
        right = 2 * i + 2
        largest = i
        if left < size and better(v.get(left), v.get(largest)):
            largest = left
        if right < size and better(v.get(right), v.get(largest)):
            largest = right
        if largest == i:
            break
        v.swap(i, largest)
        i = largest


def heap_sort(v: Vector):
    n = v.length()
    i = (n // 2) - 1
    while i >= 0:
        _down_heap(v, i, n)
        i -= 1
    end = n - 1
    while end > 0:
        v.swap(0, end)
        _down_heap(v, 0, end)
        end -= 1
    i = 0
    j = n - 1
    while i < j:
        v.swap(i, j)
        i += 1
        j -= 1


#Leaderboard Operations

class Leaderboard:
    def __init__(self):
        self.registry = PlayerRegistry()

    def cmd_add_player(self, name: str):
        if not name:
            print("ERROR: ADD_PLAYER requires a name")
            return
        if not self.registry.add_player(name):
            print("DUPLICATE")

    def cmd_add_score(self, name: str, score_str: str):
        p = self.registry.find(name)
        if p is None:
            print("NOT FOUND")
            return
        try:
            score = int(score_str)
        except Exception:
            print("ERROR: score must be an integer")
            return

        p.head = ScoreNode(score, p.head)
        if p.best is None or score > p.best:
            p.best = score

    def cmd_current(self, name: str):
        p = self.registry.find(name)
        if p is None:
            print("NOT FOUND")
            return
        current = p.head.value if p.head is not None else None
        best = p.best if p.best is not None else "NONE"
        if current is None:
            print("-> {} | current=NONE | best={}".format(p.name, best))
        else:
            print("-> {} | current={} | best={}".format(p.name, current, best))

    def cmd_best(self, name: str):
        p = self.registry.find(name)
        if p is None:
            print("NOT FOUND")
            return
        best = p.best if p.best is not None else "NONE"
        print("-> {} | best={}".format(p.name, best))

    def cmd_history(self, name: str, k_str: str):
        p = self.registry.find(name)
        if p is None:
            print("NOT FOUND")
            return
        try:
            k = int(k_str)
            if k < 0:
                raise ValueError
        except Exception:
            print("ERROR: k must be a non-negative integer")
            return
        cur = p.head
        count = 0
        if cur is None or k == 0:
            if k == 0 or cur is None:
                print("EMPTY")
            return
        while cur is not None and count < k:
            print("-> {}".format(cur.value))
            cur = cur.next
            count += 1

    def _snapshot_players(self, include_no_score_for_print_all: bool) -> Vector:
        v = Vector()
        cur = self.registry.head
        while cur is not None:
            if include_no_score_for_print_all:
                v.push_back(cur)
            else:
                if cur.best is not None:
                    v.push_back(cur)
            cur = cur.next
        return v

    def cmd_top_k(self, k_str: str):
        try:
            k = int(k_str)
            if k < 1:
                raise ValueError
        except Exception:
            print("ERROR: k must be a positive integer")
            return
        snap = self._snapshot_players(include_no_score_for_print_all=False)
        if snap.length() == 0:
            print("EMPTY")
            return
        heap_sort(snap)
        i = 0
        rank = 1
        while i < snap.length() and rank <= k:
            p = snap.get(i)
            print("-> {}. {} | best={}".format(rank, p.name, p.best))
            i += 1
            rank += 1

    def cmd_print_all(self):
        snap = self._snapshot_players(include_no_score_for_print_all=True)
        if snap.length() == 0:
            print("EMPTY")
            return
        heap_sort(snap)
        i = 0
        rank = 1
        while i < snap.length():
            p = snap.get(i)
            best = p.best if p.best is not None else "NONE"
            print("-> {}. {} | best={}".format(rank, p.name, best))
            i += 1
            rank += 1

    def cmd_remove_player(self, name: str):
        if not self.registry.remove_player(name):
            print("NOT FOUND")

    def cmd_len(self):
        print(self.registry.len())

    def cmd_clear(self):
        self.registry.clear()


#Parsing Utilities

def tokenize_line(line: str) -> Vector:

    v = Vector()
    i = 0
    n = len(line)
    while i < n and (line[i] == ' ' or line[i] == '\t' or line[i] == '\r' or line[i] == '\n'):
        i += 1
    buf = []
    in_quote = False

    while i < n:
        ch = line[i]
        if in_quote:
            if ch == '"':
                v.push_back(''.join(buf))
                buf = []
                in_quote = False
            else:
                buf.append(ch)
            i += 1
            continue
        # not in quote
        if ch == '"':
            # starting quote
            if len(buf) > 0:
                # push previous token
                v.push_back(''.join(buf))
                buf = []
            in_quote = True
            i += 1
            continue
        if ch == ' ' or ch == '\t' or ch == '\r' or ch == '\n':
            if len(buf) > 0:
                v.push_back(''.join(buf))
                buf = []
            i += 1
            while i < n and (line[i] == ' ' or line[i] == '\t' or line[i] == '\r' or line[i] == '\n'):
                i += 1
            continue
        buf.append(ch)
        i += 1

    if in_quote:
        v.push_back('"UNTERMINATED_QUOTE"')
    elif len(buf) > 0:
        v.push_back(''.join(buf))
    return v


#Command Dispatch

def process_commands(fp, program_name: str):
    lb = Leaderboard()

    for raw in fp:
        line = raw.rstrip('\n')
        j = 0
        while j < len(line) and (line[j] == ' ' or line[j] == '\t'):
            j += 1
        if j >= len(line):
            continue
        if line[j:j+1] == '#':
            continue

        # Reject quotation marks entirely (no quoted names allowed)
        if '"' in line:
            print("ERROR: quotes are not supported; use underscores for spaces")
            continue

        tokens = tokenize_line(line)
        if tokens.length() == 0:
            continue

        cmd = tokens.get(0).upper()

        if cmd == 'QUIT':
            return

        try:
            if cmd == 'ADD_PLAYER':
                if tokens.length() != 2:
                    print("ERROR: ADD_PLAYER <name>")
                else:
                    lb.cmd_add_player(tokens.get(1))

            elif cmd == 'ADD_SCORE':
                if tokens.length() != 3:
                    print("ERROR: ADD_SCORE <name> <score>")
                else:
                    lb.cmd_add_score(tokens.get(1), tokens.get(2))

            elif cmd == 'CURRENT':
                if tokens.length() != 2:
                    print("ERROR: CURRENT <name>")
                else:
                    lb.cmd_current(tokens.get(1))

            elif cmd == 'BEST':
                if tokens.length() != 2:
                    print("ERROR: BEST <name>")
                else:
                    lb.cmd_best(tokens.get(1))

            elif cmd == 'HISTORY':
                if tokens.length() != 3:
                    print("ERROR: HISTORY <name> <k>")
                else:
                    lb.cmd_history(tokens.get(1), tokens.get(2))

            elif cmd == 'TOP_K':
                if tokens.length() != 2:
                    print("ERROR: TOP_K <k>")
                else:
                    lb.cmd_top_k(tokens.get(1))

            elif cmd == 'PRINT_ALL':
                if tokens.length() != 1:
                    print("ERROR: PRINT_ALL takes no arguments")
                else:
                    lb.cmd_print_all()

            elif cmd == 'REMOVE_PLAYER':
                if tokens.length() != 2:
                    print("ERROR: REMOVE_PLAYER <name>")
                else:
                    lb.cmd_remove_player(tokens.get(1))

            elif cmd == 'LEN':
                if tokens.length() != 1:
                    print("ERROR: LEN takes no arguments")
                else:
                    lb.cmd_len()

            elif cmd == 'CLEAR':
                if tokens.length() != 1:
                    print("ERROR: CLEAR takes no arguments")
                else:
                    lb.cmd_clear()

            else:
                print("ERROR: Unknown command '{}'".format(tokens.get(0)))
        except SystemExit:
            raise
        except Exception as ex:
            # Keep going after errors as required
            print("ERROR: {}".format(str(ex)))

#Entry Point

def main(argv):
    if len(argv) != 2:
        print(USAGE)
        return 2
    path = argv[1]
    try:
        with open(path, 'r', encoding='utf-8') as f:
            process_commands(f, argv[0])
        return 0
    except Exception:
        print(USAGE)
        return 2

if __name__ == '__main__':
    sys.exit(main(sys.argv))
