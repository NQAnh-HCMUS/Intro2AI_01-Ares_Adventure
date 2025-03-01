
################################
#   LỚP GAME VÀ CÁC PHƯƠNG THỨC  #
################################

class Game:
    def __init__(self, matrix, box_weights):
        self.heuristic = 0
        self.pathSol = ""
        self.stack = []
        self.matrix = matrix
        self.box_weights = box_weights

    def __lt__(self, other):
        return self.heuristic < other.heuristic

    def load_size(self):
        max_width = max(len(row) for row in self.matrix)
        height = len(self.matrix)
        return (max_width * 32, height * 32)

    def print_matrix(self):
        for row in self.matrix:
            print("".join(row))

    def get_matrix(self):
        return self.matrix

    def is_valid_value(self, char):
        return char in [' ', '#', '@', '.', '*', '$', '+']

    def get_content(self, x, y):
        return self.matrix[y][x]

    def set_content(self, x, y, content):
        if self.is_valid_value(content):
            self.matrix[y][x] = content

    def worker(self):
        for y, row in enumerate(self.matrix):
            for x, val in enumerate(row):
                if val in ['@', '+']:
                    return (x, y, val)
        return None

    def box_list(self):
        boxes = []
        for y, row in enumerate(self.matrix):
            for x, val in enumerate(row):
                if val in ['$', '*']:
                    boxes.append((x, y))
        return boxes

    def dock_list(self):
        docks = []
        for y, row in enumerate(self.matrix):
            for x, val in enumerate(row):
                if val in ['.', '*', '+']:
                    docks.append((x, y))
        return docks

    def can_move(self, dx, dy):
        w = self.worker()
        if not w:
            return False
        wx, wy, _ = w
        content = self.get_content(wx + dx, wy + dy)
        return content not in ['#', '$', '*']

    def next(self, dx, dy):
        w = self.worker()
        if not w:
            return None
        wx, wy, _ = w
        return self.get_content(wx + dx, wy + dy)

    def can_push(self, dx, dy):
        w = self.worker()
        if not w:
            return False
        wx, wy, _ = w
        first_cell = self.get_content(wx + dx, wy + dy)
        if first_cell not in ['$', '*']:
            return False
        second_cell = self.get_content(wx + 2*dx, wy + 2*dy)
        return second_cell in [' ', '.']

    def is_completed(self):
        for row in self.matrix:
            if '$' in row:
                return False
        return True

    def move_box(self, x, y, dx, dy):
        current_box = self.get_content(x, y)
        future_box = self.get_content(x + dx, y + dy)
        if current_box == '$' and future_box == ' ':
            self.set_content(x + dx, y + dy, '$')
            self.set_content(x, y, ' ')
        elif current_box == '$' and future_box == '.':
            self.set_content(x + dx, y + dy, '*')
            self.set_content(x, y, ' ')
        elif current_box == '*' and future_box == ' ':
            self.set_content(x + dx, y + dy, '$')
            self.set_content(x, y, '.')
        elif current_box == '*' and future_box == '.':
            self.set_content(x + dx, y + dy, '*')
            self.set_content(x, y, '.')

    def unmove(self):
        if len(self.stack) > 0:
            movement = self.stack.pop()
            if movement[2]:
                current = self.worker()
                self.move(movement[0] * -1, movement[1] * -1, False)
                self.move_box(current[0] + movement[0], current[1] + movement[1],
                              movement[0] * -1, movement[1] * -1)
            else:
                self.move(movement[0] * -1, movement[1] * -1, False)

    def move(self, dx, dy, save):
        if self.can_move(dx, dy):
            wx, wy, wv = self.worker()
            future = self.next(dx, dy)
            if wv == '@' and future == ' ':
                self.set_content(wx + dx, wy + dy, '@')
                self.set_content(wx, wy, ' ')
                if save: self.stack.append((dx, dy, False))
            elif wv == '@' and future == '.':
                self.set_content(wx + dx, wy + dy, '+')
                self.set_content(wx, wy, ' ')
                if save: self.stack.append((dx, dy, False))
            elif wv == '+' and future == ' ':
                self.set_content(wx + dx, wy + dy, '@')
                self.set_content(wx, wy, '.')
                if save: self.stack.append((dx, dy, False))
            elif wv == '+' and future == '.':
                self.set_content(wx + dx, wy + dy, '+')
                self.set_content(wx, wy, '.')
                if save: self.stack.append((dx, dy, False))
        elif self.can_push(dx, dy):
            wx, wy, wv = self.worker()
            # Gọi move_box để cập nhật vị trí của box
            self.move_box(wx + dx, wy + dy, dx, dy)
            # Worker di chuyển vào vị trí cũ của box
            if wv == '@':
                self.set_content(wx, wy, ' ')
            else:
                self.set_content(wx, wy, '.')
            # Worker di chuyển đến vị trí box vừa được đẩy
            next_cell = self.get_content(wx + dx, wy + dy)
            if next_cell == '.':
                self.set_content(wx + dx, wy + dy, '+')
            else:
                self.set_content(wx + dx, wy + dy, '@')
            if save:
                self.stack.append((dx, dy, True))

    def move_with_cost(self, dx, dy, save):
        cost = 1
        if self.can_push(dx, dy):
            wx, wy, _ = self.worker()
            box_x = wx + dx
            box_y = wy + dy
            weight = self.box_weights.get((box_x, box_y), 1)
            cost += weight
            new_box_x = box_x + dx
            new_box_y = box_y + dy
            self.box_weights[(new_box_x, new_box_y)] = weight
            if (box_x, box_y) in self.box_weights:
                del self.box_weights[(box_x, box_y)]
        self.move(dx, dy, save)
        return cost