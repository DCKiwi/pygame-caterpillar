import pygame
import random

# Define some colors
black = (0, 0, 0)
white = (255, 255, 255)
green = (0, 255, 0)
red = (255, 0, 0)
yellow = (255, 255, 0)
purple = (255, 0, 255)

face_width = 40
segment_width = 35
step = 2
left_edge = 0
right_edge = 1000


class caterpillar:
    def __init__(self):
        x = random.randrange(0, 1000)
        self.face_xcoord = x
        self.face_ycoord = 250
        self.body = segment_queue()
        self.food = food_list()
        self.consumption = 0
        self.face_size = 1
        t = random.randrange(0, 2)
        if t == 0:
            self.travel_direction = 'left'
        else:
            self.travel_direction = 'right'

    def draw_caterpillar(self, screen):
        self.draw_face(screen)
        self.draw_body(screen)
        self.draw_food(screen)

    def draw_face(self, screen, colour=red):
        x = self.face_xcoord
        y = self.face_ycoord
        size = self.face_size
        pygame.draw.ellipse(screen, colour, [x, y, 40 * size, 45 * size])
        pygame.draw.ellipse(screen, black, [x + 6 * size, y + 10 * size, 10, 15])
        pygame.draw.ellipse(screen, black, [x + 24 * size, y + 10 * size, 10, 15])
        pygame.draw.line(screen, black, (x + 11 * size, y), (x + 9 * size, y - (10 * size)), 3)
        pygame.draw.line(screen, black, (x + 24 * size, y), (x + 26 * size, y - (10 * size)), 3)

    def draw_body(self, screen):

        # traverse the segment queue
        current_node = self.body.head

        while current_node is not None:

            # if consumption increases change object accordingly
            if self.consumption < 15:
                current_node.draw_segment(screen)
            elif self.consumption < 30:
                current_node.draw_segment(screen, yellow)
            else:
                self.moult(screen)

            current_node = current_node.next

    def draw_food(self, screen):
        # traverse the segment queue
        current_node = self.food.head
        while current_node is not None:
            current_node.draw_fooditem(screen)
            current_node = current_node.next

    def eat_food(self):

        # food list must be equal or greater than 1.
        if self.food.length == 0:
            return

        if self.food.length >= 1:

            # set variable to current node.
            current_food = self.food.head

            # iterate through nodes checking to see if face is 5 pixels from food.
            while current_food is not None:

                if abs(self.face_xcoord - current_food.xcoord) <= 5:
                    self.food.remove_items(current_food)
                    self.consumption += 1

                current_food = current_food.next

    def grow(self):

        # initiate Y variables as same as object face Y coordinate.
        segment_ycoord = self.face_ycoord

        # depending on segment location and travel direction segment coordinates are calculated by adding
        # face/segment width or subtracting segment width.
        if self.travel_direction == "left":

            if self.body.length == 0:
                segment_xcoord = self.face_xcoord + face_width
            else:
                segment_xcoord = self.body.last.xcoord + segment_width

        else:

            if self.body.length == 0:
                segment_xcoord = self.face_xcoord - segment_width
            else:
                segment_xcoord = self.body.last.xcoord - segment_width

        # call addSegment method with current segment X & Y coordinates.
        self.body.addSegment(segment_xcoord, segment_ycoord)

    def reverse(self):

        # call reverse method on object
        self.body.reverseQueue()

        # change travel direction and head coordinates accordingly.
        if self.travel_direction == "left":
            self.travel_direction = "right"
            self.face_xcoord = self.body.head.xcoord + segment_width
        else:
            self.travel_direction = "left"
            self.face_xcoord = self.body.head.xcoord - face_width

    def move_forward(self):

        # if object has no body object cant move.
        if self.body.length == 0:
            return

        if self.travel_direction == "left":

            # call reverse if object at left screen edge.
            if self.face_xcoord < left_edge:
                self.reverse()
                return

            # increment face coordinates by -step
            self.face_xcoord -= step

            # traverse queue, increment each segment node by -step
            self.body.traverseQueue(-step)
        else:

            # call reverse if object at right screen edge.
            if self.face_xcoord > right_edge - face_width:
                self.reverse()
                return

            # increment face coordinates by step
            self.face_xcoord += step

            # traverse queue, increment each segment node by +step.
            self.body.traverseQueue(step)

        # call eat food method as caterpillar moves
        self.eat_food()

    def drop_food(self):

        # initiate variables for random food location.
        food_xcoord = random.randrange(0, 950)
        food_ycoord = random.randrange(self.face_ycoord, self.face_ycoord + face_width)

        # call add food method with random coordinates.
        self.food.add_food(food_xcoord, food_ycoord)

    def moult(self, screen):

        # adjust face object
        self.face_ycoord = 208
        self.face_size = 1.5
        self.draw_face(screen, green)

        # traverse queue and adjust body segment and face
        current_node = self.body.head

        while current_node is not None:
            current_node.draw_segment(screen, body=white, size=2)
            current_node.ycoord = 208

            if self.travel_direction == "left":
                self.face_xcoord = self.body.head.xcoord - (face_width * 1.5)
            else:
                self.face_xcoord = self.body.head.xcoord + (segment_width * 2)

            current_node = current_node.next


class segment_queue:
    def __init__(self):
        self.length = 0
        self.head = None
        self.last = None

    def isEmpty(self):
        return self.length == 0

    def addSegment(self, x, y):

        # initiate segment variable with node.
        segment = body_segment(x, y)
        segment.next = None

        # Improved Linked Queue implementation
        if self.length == 0:
            self.head = self.last = segment
        else:
            last = self.last
            last.next = segment
            self.last = segment

        self.length = self.length + 1

    def traverseQueue(self, x):

        # traverse queue and increment X coordinates.
        current_node = self.head

        while current_node:
            current_node.xcoord += x
            current_node = current_node.next

    def reverseQueue(self):

        # reverse order of queue
        b = None
        t = self.head

        while t != None:
            a = t.next
            t.next = b
            b = t
            t = a

        self.last = self.head
        self.head = b


class body_segment:
    def __init__(self, x, y):
        self.xcoord = x
        self.ycoord = y
        self.next = None

    def draw_segment(self, screen, body=green, size=1):
        x = self.xcoord
        y = self.ycoord
        pygame.draw.ellipse(screen, body, [x, y, 35 * size, 40 * size])
        pygame.draw.line(screen, black, (x + 8 * size, y + 35 * size), (x + 8 * size, y + 45 * size), 3)
        pygame.draw.line(screen, black, (x + 24 * size, y + 35 * size), (x + 24 * size, y + 45 * size), 3)


class food_list:
    def __init__(self):
        self.length = 0
        self.head = None

    def add_food(self, x, y):

        # initiate food item variable with node and add to linked list.
        item = food_item(x, y)
        item.next = self.head
        self.head = item
        self.length += 1

    # removes items from front of linked list.
    def remove_first(self):

        if self.head is not None:
            self.head = self.head.next
            self.length -= 1

    # removes items from middle of linked list.
    def remove_item(self, pos):
        if pos.next is not None:
            pos.next = pos.next.next
            self.length -= 1

    # combines previous two methods into one method
    def remove_items(self, value):

        while self.head is not None and self.head == value:
            self.remove_first()

        pred = self.head

        while pred is not None:
            while pred.next is not None and pred.next == value:
                self.remove_item(pred)

            pred = pred.next


class food_item:
    def __init__(self, x, y):
        self.xcoord = x
        self.ycoord = y
        self.next = None

    def draw_fooditem(self, screen):
        x = self.xcoord
        y = self.ycoord
        pygame.draw.ellipse(screen, yellow, [x, y, 15, 15])


