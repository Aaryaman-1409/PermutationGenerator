import random
import re
from django.contrib import messages
import numpy as np


class TwoLine:
    def __init__(self, size: int, permutation=None):
        self.size = size
        if permutation is None:
            self.permutation = self.generate_perms()
        else:
            self.permutation = permutation

    def generate_perms(self):
        _perm = {x + 1: x + 1 for x in range(self.size)}
        shuffled = list(_perm.values())
        shuffled_dict = dict(zip(_perm, shuffled))
        while all(v == k for v, k in shuffled_dict.items()):
            random.shuffle(shuffled)
            shuffled_dict = dict(zip(_perm, shuffled))
        return shuffled_dict

    def to_latex(self):
        topline = [x + 1 for x in range(self.size)]
        botline = [self.permutation[x] for x in topline]
        s = r'$$\begin{pmatrix}'
        for x in topline:
            s += (str(x) + '&')
        s += r"\\"
        s = s.replace(r'&\\', r"\\")
        for x in botline:
            s += (str(x) + '&')
        s += r"\end{pmatrix}"
        s = s.replace(r'&\end{pmatrix}', r"\end{pmatrix}$$")

        return s


class Solution:
    def __init__(self, two_line_dict, student_input=None):
        self.two_line = two_line_dict
        self.size = len(self.two_line)
        self.student_input = student_input

    def to_disjoint_cycle(self):
        cyclic = []
        perm = self.two_line.copy()
        perm_keys = list(perm.keys())
        for key in perm_keys:
            val = perm.pop(key, None)
            if val is None:
                continue
            cycle = str(key)
            while key != val:
                cycle += str(val)
                val = perm.pop(val)
            cyclic.append(cycle)
        removed_singles = [x for x in cyclic if len(x) != 1]
        return removed_singles

    def to_two_line(self):
        two_line = {}
        for cycle in self.student_input:
            for count, value in enumerate(cycle):
                if count == len(cycle) - 1:
                    two_line[int(value)] = int(cycle[0])
                    break
                two_line[int(value)] = int(cycle[count + 1])

        for x in range(self.size):
            if x + 1 in two_line:
                continue

            two_line[x + 1] = x + 1

        return two_line


class Cyclic(Solution):
    def __init__(self, two_line_obj, student_input):
        super().__init__(two_line_obj, student_input)

    def solution(self):
        s = ''
        for x in self.to_disjoint_cycle():
            s += '(' + x + ')'
        return s

    def check_answer(self, request):
        if self.to_two_line() == self.two_line:
            messages.success(request, "Correct Answer", extra_tags='cyclic')
        else:
            messages.error(request, 'Wrong Answer', extra_tags='cyclic')
            messages.error(request, 'Actual Solution: ' + str(self.solution()), extra_tags='cyclic')


class Order(Solution):
    def __init__(self, two_line_obj, student_input):
        super().__init__(two_line_obj, student_input)

    def solution(self):
        lengths = [len(x) for x in self.to_disjoint_cycle()]
        return int(np.lcm.reduce(lengths))

    def check_answer(self, request):
        if self.student_input == self.solution():
            messages.success(request, "Correct Answer", extra_tags='order')
        else:
            messages.error(request, 'Wrong Answer', extra_tags='order')
            messages.error(request, 'Actual Solution: ' + str(self.solution()), extra_tags='order')


class Sign(Solution):
    def __init__(self, two_line_obj, student_input):
        super().__init__(two_line_obj, student_input)

    def solution(self):
        disjoint_signs = [(-1) ** (len(x) - 1) for x in self.to_disjoint_cycle()]
        return int(np.prod(disjoint_signs))

    def check_answer(self, request):
        if self.student_input == self.solution():
            messages.success(request, "Correct Answer", extra_tags='sign')
        else:
            messages.error(request, 'Wrong Answer', extra_tags='sign')
            messages.error(request, 'Actual Solution: ' + str(self.solution()), extra_tags='sign')


class Inverse(Solution):
    def __init__(self, two_line_obj, student_input):  # input will be array of numbers
        super().__init__(two_line_obj, student_input)

    def solution(self):
        unsorted = {v: k for k, v in self.two_line.items()}
        return dict(sorted(unsorted.items()))

    def check_answer(self, request):
        student_dict = dict(zip([i + 1 for i in range(len(self.student_input))], self.student_input))
        if student_dict == self.solution():
            messages.success(request, "Correct Answer", extra_tags='inverse')
        else:
            messages.error(request, 'Wrong Answer', extra_tags='inverse')
            messages.error(request, 'Actual Solution: ' + str(self.solution()), extra_tags='inverse')
