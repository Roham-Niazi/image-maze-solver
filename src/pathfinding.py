from collections import deque



#BFS algorithm
def bfs(graph, start, end):
	q=deque([[start]])
	visited={start}

	while q:
		path=q.popleft()
		node=path[-1]

		if node==end:
			return path

		for nxt in graph[node]:
			if nxt not in visited:
				visited.add(nxt)
				q.append(path+[nxt])

	return None