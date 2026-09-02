import cv2
import numpy as np
from . import pathfinding



class MazeSolver():
	def __init__(self, image_data):
		#Opening image
		img=cv2.cvtColor(image_data, cv2.COLOR_BGR2GRAY)
		bin_img=cv2.adaptiveThreshold(img, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 301, 2)

		#Removing border
		coords=cv2.findNonZero(cv2.bitwise_not(bin_img))
		x, y, w, h=cv2.boundingRect(coords)
		bin_img=bin_img[y:y+h, x:x+w]

		self.bin_img=bin_img
		self.start_pt=None
		self.end_pt=None

	def set_start_end_pt(self, base_img, pt):
		if self.start_pt==None:
			self.start_pt=pt
		else:
			self.end_pt=pt

		#Showing Point
		new_bin_img=base_img.copy()
		cv2.circle(new_bin_img, pt, 5, (0, 255, 0), -1)

		return new_bin_img


	def white_lines_masks(self, image, kernel):
		#Detecting horizontal and vertical white lines that are maze path
		horizontalStructure=cv2.getStructuringElement(cv2.MORPH_RECT, (kernel, 1))
		verticalStructure=cv2.getStructuringElement(cv2.MORPH_RECT, (1, kernel))

		mask_horizontal=cv2.morphologyEx(image, cv2.MORPH_OPEN, horizontalStructure)
		mask_vertical=cv2.morphologyEx(image, cv2.MORPH_OPEN, verticalStructure)

		return mask_vertical, mask_horizontal


	def are_connected(self, img, p1, p2):
		#Checking is there a path between two points
		line_mask=np.zeros_like(img)
		cv2.line(line_mask, p1, p2, 255, 2)

		line_pixs=img[line_mask>0]
		white_ratio=np.mean(line_pixs>0)

		return white_ratio==1



	def solve(self):
		#finding best kernel value
		pix_cnt=self.bin_img.shape[0]*self.bin_img.shape[1]
		last_mask_pix_cnt=None
		changes=[]
		for k in range(1, 102, 2):
			mask_vertical, mask_horizontal=self.white_lines_masks(self.bin_img, k)
			points_mask=cv2.bitwise_and(mask_horizontal, mask_horizontal, mask=mask_vertical)
			mask_pix_cnt=np.count_nonzero(points_mask)

			if last_mask_pix_cnt!=None:
				change=last_mask_pix_cnt-mask_pix_cnt
				change_perc=change/pix_cnt*100
				changes.append((k, change_perc))

			last_mask_pix_cnt=mask_pix_cnt

		#Selecting most changed as best kernel
		best_k=max(changes, key=lambda x: x[1])[0]

		#Detecting vertical and horizontal white lines and their intersection points
		mask_vertical, mask_horizontal=self.white_lines_masks(self.bin_img, best_k)
		points_mask=cv2.bitwise_and(mask_horizontal, mask_horizontal, mask=mask_vertical)


		#Determining center point of each intersection point
		contours, _=cv2.findContours(points_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

		key_pts=[self.start_pt, self.end_pt]
		for cnt in contours:
			x, y, w, h=cv2.boundingRect(cnt)

			center=(x+w//2, y+h//2)
			key_pts.append(center)


		#Creating graph of maze
		graph={p: [] for p in range(len(key_pts))}
		for p1_idx in range(len(key_pts)):
			for p2_idx in range(p1_idx+1, len(key_pts)):
				p1=key_pts[p1_idx]
				p2=key_pts[p2_idx]
				if self.are_connected(self.bin_img, p1, p2):
					graph[p1_idx].append(p2_idx)
					graph[p2_idx].append(p1_idx)


		#Finding path
		path=pathfinding.bfs(graph, key_pts.index(self.start_pt), key_pts.index(self.end_pt))

		if path==None: return None

		#Showing path on maze image
		output_img=cv2.cvtColor(self.bin_img, cv2.COLOR_GRAY2RGB)
		for i in range(len(path)-1):
			p1_idx=path[i]
			p2_idx=path[i+1]

			cv2.line(output_img, key_pts[p1_idx], key_pts[p2_idx], (0, 0, 255), 2)

		return output_img