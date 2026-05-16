"""
test_dsa.py — Automated Unit Tests for DSA Explorer & Visualiser
Covers Phase 1 (Data Structures), Phase 2 (Sorting + Heap), Phase 3 (Pathfinding + DP)

Run with:
    python -m unittest test_dsa.py -v
"""

import unittest

# PHASE 1 — DATA STRUCTURES


# Import logic classes only — no Pygame needed for unit tests
from Data_Structures_module import Stack, Queue, LinkedList, BST


class TestStack(unittest.TestCase):
    """Tests for Stack push/pop behaviour."""

    def test_push_increases_size(self):
        """Pushing an item should increase stack size by 1."""
        s = Stack()
        s.push(1)
        self.assertEqual(len(s.stack), 1)

    def test_push_pop_sequence(self):
        """Push 3 items, pop 2 — final size should be 1 with correct order."""
        s = Stack()
        s.push("A")
        s.push("B")
        s.push("C")
        self.assertEqual(s.pop(), "C")  # LIFO — last in first out
        self.assertEqual(s.pop(), "B")
        self.assertEqual(len(s.stack), 1)
        self.assertEqual(s.stack[0], "A")

    def test_pop_empty_returns_none(self):
        """Popping from empty stack should return None not raise an error."""
        s = Stack()
        self.assertIsNone(s.pop())

    def test_peek_does_not_remove(self):
        """Peek should return top item without removing it."""
        s = Stack()
        s.push(42)
        self.assertEqual(s.peek(), 42)
        self.assertEqual(len(s.stack), 1)

    def test_is_empty(self):
        """isEmpty should return True on new stack, False after push."""
        s = Stack()
        self.assertTrue(s.is_empty())
        s.push(1)
        self.assertFalse(s.is_empty())

    def test_is_full(self):
        """Stack should be full at MAX_CAPACITY (9) items."""
        s = Stack()
        for i in range(9):
            s.push(i)
        self.assertTrue(s.is_full())

    def test_lifo_order(self):
        """Items should come out in last-in-first-out order."""
        s = Stack()
        for i in [10, 20, 30]:
            s.push(i)
        result = [s.pop() for _ in range(3)]
        self.assertEqual(result, [30, 20, 10])


class TestQueue(unittest.TestCase):
    """Tests for Queue enqueue/dequeue behaviour."""

    def test_enqueue_increases_size(self):
        """Enqueueing should increase queue size."""
        q = Queue()
        q.enqueue(1)
        self.assertEqual(len(q.queue), 1)

    def test_enqueue_dequeue_fifo(self):
        """Enqueue 4 items, dequeue 3 — FIFO order must be maintained."""
        q = Queue()
        for v in [1, 2, 3, 4]:
            q.enqueue(v)
        self.assertEqual(q.dequeue(), 1)
        self.assertEqual(q.dequeue(), 2)
        self.assertEqual(q.dequeue(), 3)
        self.assertEqual(len(q.queue), 1)
        self.assertEqual(q.queue[0], 4)

    def test_dequeue_empty_returns_none(self):
        """Dequeuing from empty queue should return None."""
        q = Queue()
        self.assertIsNone(q.dequeue())

    def test_is_empty(self):
        """isEmpty should return True on new queue, False after enqueue."""
        q = Queue()
        self.assertTrue(q.is_empty())
        q.enqueue("x")
        self.assertFalse(q.is_empty())

    def test_is_full(self):
        """Queue should be full at MAX_CAPACITY (9) items."""
        q = Queue()
        for i in range(9):
            q.enqueue(i)
        self.assertTrue(q.is_full())

    def test_fifo_order_preserved(self):
        """All items should come out in the order they went in."""
        q = Queue()
        items = [5, 3, 8, 1, 2]
        for i in items:
            q.enqueue(i)
        result = [q.dequeue() for _ in range(len(items))]
        self.assertEqual(result, items)


class TestLinkedList(unittest.TestCase):
    """Tests for LinkedList insert/delete/reverse."""

    def test_insert_single(self):
        """Inserting one node should produce a list of length 1."""
        ll = LinkedList()
        ll.insert(10)
        self.assertEqual(ll.to_list(), [10])

    def test_insert_at_position(self):
        """Insert node with value 10 — node should be present in correct location."""
        ll = LinkedList()
        ll.insert(1)
        ll.insert(10)  # position 2 (0-indexed: position 1)
        ll.insert(3)
        result = ll.to_list()
        self.assertIn(10, result)
        self.assertEqual(result[1], 10)

    def test_insert_multiple_order(self):
        """Nodes should appear in insertion order."""
        ll = LinkedList()
        for v in [1, 2, 3]:
            ll.insert(v)
        self.assertEqual(ll.to_list(), [1, 2, 3])

    def test_delete_head(self):
        """Deleting the head node should update head correctly."""
        ll = LinkedList()
        ll.insert(1)
        ll.insert(2)
        ll.delete(1)
        self.assertEqual(ll.to_list(), [2])

    def test_delete_middle(self):
        """Deleting a middle node should keep others intact."""
        ll = LinkedList()
        for v in [1, 2, 3]:
            ll.insert(v)
        ll.delete(2)
        self.assertEqual(ll.to_list(), [1, 3])

    def test_delete_nonexistent(self):
        """Deleting a value not in list should not raise an error."""
        ll = LinkedList()
        ll.insert(1)
        ll.delete(99)  # should do nothing
        self.assertEqual(ll.to_list(), [1])

    def test_reverse(self):
        """Reversing should return items in reverse insertion order."""
        ll = LinkedList()
        for v in [1, 2, 3]:
            ll.insert(v)
        ll.reverse()
        self.assertEqual(ll.to_list(), [3, 2, 1])

    def test_reverse_empty(self):
        """Reversing empty list should not raise an error."""
        ll = LinkedList()
        ll.reverse()
        self.assertEqual(ll.to_list(), [])


class TestBST(unittest.TestCase):
    """Tests for Binary Search Tree insert and traversals."""

    def test_inorder_traversal(self):
        """Insert [50, 30, 70] — inorder traversal should return [30, 50, 70]."""
        bst = BST()
        for v in [50, 30, 70]:
            bst.insert(v)
        self.assertEqual(bst.inorder(), [30, 50, 70])

    def test_preorder_traversal(self):
        """Insert [50, 30, 70] — preorder should return [50, 30, 70]."""
        bst = BST()
        for v in [50, 30, 70]:
            bst.insert(v)
        self.assertEqual(bst.preorder(), [50, 30, 70])

    def test_postorder_traversal(self):
        """Insert [50, 30, 70] — postorder should return [30, 70, 50]."""
        bst = BST()
        for v in [50, 30, 70]:
            bst.insert(v)
        self.assertEqual(bst.postorder(), [30, 70, 50])

    def test_no_duplicates(self):
        """Inserting a duplicate value should not add a second node."""
        bst = BST()
        bst.insert(10)
        bst.insert(10)
        self.assertEqual(bst.inorder(), [10])

    def test_left_subtree(self):
        """Values less than root should go to the left subtree."""
        bst = BST()
        bst.insert(50)
        bst.insert(20)
        self.assertEqual(bst.root.left.val, 20)

    def test_right_subtree(self):
        """Values greater than root should go to the right subtree."""
        bst = BST()
        bst.insert(50)
        bst.insert(80)
        self.assertEqual(bst.root.right.val, 80)

    def test_inorder_sorted(self):
        """Inorder traversal of any BST should always return sorted values."""
        bst = BST()
        values = [40, 20, 60, 10, 30, 50, 70]
        for v in values:
            bst.insert(v)
        self.assertEqual(bst.inorder(), sorted(values))


# PHASE 2 — SORTING ALGORITHMS


from sorting_module import bubble_sort, selection_sort, mergesort


class TestBubbleSort(unittest.TestCase):
    """Tests for bubble sort correctness."""

    def test_spec_case(self):
        """Spec test: sort [5,3,8,1,2] → [1,2,3,5,8]."""
        arr = [5, 3, 8, 1, 2]
        bubble_sort(arr)
        self.assertEqual(arr, [1, 2, 3, 5, 8])

    def test_already_sorted(self):
        """Already sorted array should remain sorted."""
        arr = [1, 2, 3, 4, 5]
        bubble_sort(arr)
        self.assertEqual(arr, [1, 2, 3, 4, 5])

    def test_reverse_sorted(self):
        """Reverse sorted array should sort correctly."""
        arr = [5, 4, 3, 2, 1]
        bubble_sort(arr)
        self.assertEqual(arr, [1, 2, 3, 4, 5])

    def test_single_element(self):
        """Single element array should be unchanged."""
        arr = [42]
        bubble_sort(arr)
        self.assertEqual(arr, [42])

    def test_empty(self):
        """Empty array should remain empty."""
        arr = []
        bubble_sort(arr)
        self.assertEqual(arr, [])

    def test_duplicates(self):
        """Array with duplicates should sort correctly."""
        arr = [3, 1, 2, 1, 3]
        bubble_sort(arr)
        self.assertEqual(arr, [1, 1, 2, 3, 3])


class TestSelectionSort(unittest.TestCase):
    """Tests for selection sort correctness."""

    def test_spec_case(self):
        """Sort [5,3,8,1,2] → [1,2,3,5,8]."""
        arr = [5, 3, 8, 1, 2]
        selection_sort(arr)
        self.assertEqual(arr, [1, 2, 3, 5, 8])

    def test_already_sorted(self):
        arr = [1, 2, 3, 4, 5]
        selection_sort(arr)
        self.assertEqual(arr, [1, 2, 3, 4, 5])

    def test_reverse_sorted(self):
        arr = [5, 4, 3, 2, 1]
        selection_sort(arr)
        self.assertEqual(arr, [1, 2, 3, 4, 5])

    def test_duplicates(self):
        arr = [3, 1, 2, 1, 3]
        selection_sort(arr)
        self.assertEqual(arr, [1, 1, 2, 3, 3])

    def test_single_element(self):
        arr = [7]
        selection_sort(arr)
        self.assertEqual(arr, [7])


class TestMergeSort(unittest.TestCase):
    """Tests for merge sort correctness."""

    def test_spec_case(self):
        """Sort [5,3,8,1,2] → [1,2,3,5,8]."""
        arr = [5, 3, 8, 1, 2]
        mergesort(arr, 0, len(arr) - 1)
        self.assertEqual(arr, [1, 2, 3, 5, 8])

    def test_already_sorted(self):
        arr = [1, 2, 3, 4, 5]
        mergesort(arr, 0, len(arr) - 1)
        self.assertEqual(arr, [1, 2, 3, 4, 5])

    def test_reverse_sorted(self):
        arr = [5, 4, 3, 2, 1]
        mergesort(arr, 0, len(arr) - 1)
        self.assertEqual(arr, [1, 2, 3, 4, 5])

    def test_duplicates(self):
        arr = [3, 1, 2, 1, 3]
        mergesort(arr, 0, len(arr) - 1)
        self.assertEqual(arr, [1, 1, 2, 3, 3])

    def test_single_element(self):
        arr = [99]
        mergesort(arr, 0, 0)
        self.assertEqual(arr, [99])

    def test_large_random(self):
        """Merge sort result should match Python's built-in sort."""
        import random

        arr = random.sample(range(1000), 50)
        expected = sorted(arr)
        mergesort(arr, 0, len(arr) - 1)
        self.assertEqual(arr, expected)


#  PHASE 2 — HEAP


from heap_module import MaxHeap


class TestMaxHeap(unittest.TestCase):
    """Tests for MaxHeap insert and extract."""

    def test_insert_single(self):
        """Inserting one item — heap should have size 1."""
        h = MaxHeap()
        h.insert_heap(10)
        self.assertEqual(len(h), 1)

    def test_max_at_root(self):
        """After inserting [10, 20, 5], root should be 20 (max)."""
        h = MaxHeap()
        for v in [10, 20, 5]:
            h.insert_heap(v)
        self.assertEqual(h._arr[0], 20)

    def test_extract_returns_max(self):
        """Extract should return the largest value."""
        h = MaxHeap()
        for v in [10, 20, 5]:
            h.insert_heap(v)
        self.assertEqual(h.remove_heap(), 20)

    def test_extract_reorders(self):
        """After extracting max, new max should be at root."""
        h = MaxHeap()
        for v in [10, 20, 5]:
            h.insert_heap(v)
        h.remove_heap()
        self.assertEqual(h._arr[0], 10)

    def test_extract_all_sorted(self):
        """Extracting all items should return them in descending order."""
        h = MaxHeap()
        values = [3, 1, 4, 1, 5, 9, 2, 6]
        for v in values:
            h.insert_heap(v)
        result = [h.remove_heap() for _ in range(len(values))]
        self.assertEqual(result, sorted(values, reverse=True))

    def test_extract_empty_raises(self):
        """Extracting from empty heap should raise an exception."""
        h = MaxHeap()
        with self.assertRaises(Exception):
            h.remove_heap()

    def test_is_empty(self):
        """New heap should be empty."""
        h = MaxHeap()
        self.assertTrue(h.isEmpty())

    def test_heap_grows(self):
        """Heap should grow dynamically beyond initial size."""
        h = MaxHeap()
        for v in range(20):
            h.insert_heap(v)
        self.assertEqual(len(h), 20)
        self.assertEqual(h._arr[0], 19)


# PHASE 3 — PATHFINDING + DP


from puzzles_module import (
    dijkstra_steps,
    astar_steps,
    dp_path_count,
    make_grid,
    make_dp_grid,
    GRID_ROWS,
    GRID_COLS,
    DP_ROWS,
    DP_COLS,
)


class TestDijkstra(unittest.TestCase):
    """Tests for Dijkstra pathfinding."""

    def _run_to_completion(self, gen):
        """Exhaust a pathfinding generator and return the final state."""
        visited, frontier, path = set(), set(), []
        for visited, frontier, path in gen:
            pass
        return visited, path

    def test_finds_path_open_grid(self):
        """Dijkstra should find a path on an open grid."""
        grid = make_grid()
        start = (0, 0)
        end = (3, 3)
        _, path = self._run_to_completion(dijkstra_steps(grid, start, end))
        self.assertIn(start, path)
        self.assertIn(end, path)

    def test_no_path_when_blocked(self):
        """Dijkstra should return empty path when end is completely blocked."""
        grid = make_grid()
        # Wall off cell (0,1) and (1,0) — trapping start (0,0)
        grid[0][1] = 1
        grid[1][0] = 1
        start = (0, 0)
        end = (3, 3)
        _, path = self._run_to_completion(dijkstra_steps(grid, start, end))
        self.assertEqual(path, [])

    def test_start_equals_end(self):
        """When start equals end, path should contain just that cell."""
        grid = make_grid()
        start = (0, 0)
        _, path = self._run_to_completion(dijkstra_steps(grid, start, start))
        self.assertIn(start, path)

    def test_path_is_connected(self):
        """Each step in the path should be adjacent to the next."""
        grid = make_grid()
        start = (0, 0)
        end = (2, 2)
        _, path = self._run_to_completion(dijkstra_steps(grid, start, end))
        for i in range(len(path) - 1):
            r1, c1 = path[i]
            r2, c2 = path[i + 1]
            self.assertEqual(abs(r1 - r2) + abs(c1 - c2), 1)


class TestAstar(unittest.TestCase):
    """Tests for A* pathfinding."""

    def _run_to_completion(self, gen):
        visited, frontier, path = set(), set(), []
        for visited, frontier, path in gen:
            pass
        return visited, path

    def test_finds_path_open_grid(self):
        """A* should find a path on an open grid."""
        grid = make_grid()
        start = (0, 0)
        end = (3, 3)
        _, path = self._run_to_completion(astar_steps(grid, start, end))
        self.assertIn(start, path)
        self.assertIn(end, path)

    def test_same_result_as_dijkstra(self):
        """A* and Dijkstra should find paths of equal length on open grids."""
        grid = make_grid()
        start = (0, 0)
        end = (4, 4)
        _, d_path = self._run_to_completion(dijkstra_steps(grid, start, end))
        _, a_path = self._run_to_completion(astar_steps(grid, start, end))
        self.assertEqual(len(d_path), len(a_path))

    def test_no_path_when_blocked(self):
        """A* should return empty path when end is unreachable."""
        grid = make_grid()
        grid[0][1] = 1
        grid[1][0] = 1
        start = (0, 0)
        end = (3, 3)
        _, path = self._run_to_completion(astar_steps(grid, start, end))
        self.assertEqual(path, [])


class TestDPGrid(unittest.TestCase):
    """Tests for DP path counting."""

    def test_open_grid_has_paths(self):
        """Open grid should have at least one path from start to end."""
        grid = [[0] * DP_COLS for _ in range(DP_ROWS)]
        dp, path = dp_path_count(grid)
        self.assertGreater(dp[DP_ROWS - 1][DP_COLS - 1], 0)

    def test_fully_blocked_row(self):
        """A fully blocked row should result in zero paths."""
        grid = [[0] * DP_COLS for _ in range(DP_ROWS)]
        grid[2] = [1] * DP_COLS  # wall across entire row 2
        dp, path = dp_path_count(grid)
        self.assertEqual(dp[DP_ROWS - 1][DP_COLS - 1], 0)

    def test_single_cell_grid(self):
        """1x1 grid — only one path (start = end)."""
        grid = [[0]]
        dp, path = dp_path_count(grid)
        self.assertEqual(dp[0][0], 1)

    def test_path_starts_at_origin(self):
        """Reconstructed path should include (0, 0)."""
        grid = [[0] * DP_COLS for _ in range(DP_ROWS)]
        _, path = dp_path_count(grid)
        self.assertIn((0, 0), path)

    def test_path_ends_at_destination(self):
        """Reconstructed path should include the bottom-right cell."""
        grid = [[0] * DP_COLS for _ in range(DP_ROWS)]
        _, path = dp_path_count(grid)
        self.assertIn((DP_ROWS - 1, DP_COLS - 1), path)

    def test_simple_2x2(self):
        """2x2 open grid should have exactly 2 paths (right-down, down-right)."""
        grid = [[0, 0], [0, 0]]
        dp, _ = dp_path_count(grid)
        self.assertEqual(dp[1][1], 2)

    def test_obstacle_reduces_paths(self):
        """Adding an obstacle should reduce the number of available paths."""
        open_grid = [[0] * DP_COLS for _ in range(DP_ROWS)]
        dp_open, _ = dp_path_count(open_grid)
        open_count = dp_open[DP_ROWS - 1][DP_COLS - 1]

        blocked_grid = [[0] * DP_COLS for _ in range(DP_ROWS)]
        blocked_grid[1][1] = 1  # add one obstacle
        dp_blocked, _ = dp_path_count(blocked_grid)
        blocked_count = dp_blocked[DP_ROWS - 1][DP_COLS - 1]

        self.assertLess(blocked_count, open_count)


if __name__ == "__main__":
    unittest.main(verbosity=2)
