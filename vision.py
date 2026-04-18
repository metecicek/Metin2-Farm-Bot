import cv2
import numpy as np


class Vision:
    def __init__(self, img_path=None, method=cv2.TM_CCOEFF_NORMED):
        self.method = method
        self.template = None
        self.w = 0
        self.h = 0

        if img_path:
            img = cv2.imread(img_path, cv2.IMREAD_UNCHANGED)

            if img is None:
                raise ValueError(f"Template not found: {img_path}")

            # Alpha channel fix
            if len(img.shape) == 3 and img.shape[-1] == 4:
                img = cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)

            self.template = img
            self.h, self.w = img.shape[:2]

    def find(self, img, threshold=0.6):
        """
        Stabil template matching
        """
        if self.template is None:
            return []

        if img is None or img.size == 0:
            return []

        result = cv2.matchTemplate(img, self.template, self.method)

        yloc, xloc = np.where(result >= threshold)

        rects = []

        for (x, y) in zip(xloc, yloc):
            rects.append((int(x), int(y), self.w, self.h))

        # duplicate removal (overlap fix)
        rects = self._group_rects(rects)

        return rects

    def _group_rects(self, rects):
        """
        Overlapping box cleanup (stabil detection)
        """
        if len(rects) == 0:
            return []

        boxes = []
        for (x, y, w, h) in rects:
            boxes.append([x, y, w, h])
            boxes.append([x, y, w, h])  # groupRectangles fix trick

        grouped, _ = cv2.groupRectangles(boxes, groupThreshold=1, eps=0.5)

        return grouped.tolist() if len(grouped) > 0 else []

    def get_click_points(self, rects):
        """
        Safe center calculation
        """
        points = []

        for (x, y, w, h) in rects:
            cx = x + w // 2
            cy = y + h // 2
            points.append((cx, cy))

        return points

    def draw_rectangles(self, img, rects):
        """
        Debug visualization
        """
        if img is None:
            return img

        for (x, y, w, h) in rects:
            cv2.rectangle(
                img,
                (x, y),
                (x + w, y + h),
                (0, 255, 0),
                2
            )

        return img

    def draw_crosshairs(self, img, points):
        """
        Debug points
        """
        for (x, y) in points:
            cv2.drawMarker(
                img,
                (x, y),
                (255, 0, 255),
                cv2.MARKER_CROSS,
                10,
                2
            )

        return img