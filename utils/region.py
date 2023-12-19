class Region:
    def __init__(self, x1: float = 0, y1: float = 0,
                 x2: float = 0, y2: float = 0,
                 w: float = 0, h: float = 0,
                 center_x: float = 0, center_y: float = 0,
                 expand_top: bool = True, expand_bottom: bool = True,
                 expand_left: bool = True, expand_right: bool = True) -> None:
        if x1 != 0 and y1 != 0 and x2 != 0 and y2 != 0:
            # 使用两个点表示矩形区域
            self.x1 = min(x1, x2)
            self.y1 = min(y1, y2)
            self.x2 = max(x1, x2)
            self.y2 = max(y1, y2)
            self.center_x = (x1 + x2) / 2
            self.center_y = (y1 + y2) / 2
            self.w = x2 - x1
            self.h = y2 - y1
        elif center_x != 0 and center_y != 0 and w != 0 and h != 0:
            # 使用中心点和宽高表示矩形区域
            self.center_x = center_x
            self.center_y = center_y
            self.w = w
            self.h = h
            if expand_top:
                self.y1 = center_y - h / 2
            else:
                self.y1 = center_y
            if expand_bottom:
                self.y2 = center_y + h / 2
            else:
                self.y2 = center_y
            if expand_left:
                self.x1 = center_x - w / 2
            else:
                self.x1 = center_x
            if expand_right:
                self.x2 = center_x + w / 2
            else:
                self.x2 = center_x

            # self.x1 = center_x - w / 2
            # self.y1 = center_y - h / 2
            # self.x2 = center_x + w / 2
            # self.y2 = center_y + h / 2
        else:
            raise ValueError('Invalid parameters')

    def is_in_region(self, x: float, y: float) -> bool:
        return self.x1 <= x <= self.x2 and self.y1 <= y <= self.y2
