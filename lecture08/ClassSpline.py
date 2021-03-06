class SplineTuple:
    def __init__(self, a, b, c, d, x):
        self.a = a
        self.b = b
        self.c = c
        self.d = d
        self.x = x


# Построение сплайна
# x - узлы сетки, должны быть упорядочены по возрастанию, кратные узлы запрещены
# y - значения функции в узлах сетки
# n - количество узлов сетки
def BuildSpline(x, y, n):
    # Инициализация массива сплайнов
    splines = [SplineTuple(0, 0, 0, 0, 0) for _ in range(0, n)]
    for i in range(0, n):
        splines[i].x = x[i]
        splines[i].a = y[i]

    splines[0].c = splines[n - 1].c = 0.0

    # Решение СЛАУ относительно коэффициентов сплайнов c[i] методом прогонки для трехдиагональных матриц
    # Вычисление прогоночных коэффициентов - прямой ход метода прогонки
    alpha = [0.0 for _ in range(0, n - 1)]
    beta = [0.0 for _ in range(0, n - 1)]

    for i in range(1, n - 1):
        hi = x[i] - x[i - 1]
        hi1 = x[i + 1] - x[i]
        A = hi
        C = 2.0 * (hi + hi1)
        B = hi1
        F = 6.0 * ((y[i + 1] - y[i]) / hi1 - (y[i] - y[i - 1]) / hi)
        z = (A * alpha[i - 1] + C)
        alpha[i] = -B / z
        beta[i] = (F - A * beta[i - 1]) / z

    # Нахождение решения - обратный ход метода прогонки
    for i in range(n - 2, 0, -1):
        splines[i].c = alpha[i] * splines[i + 1].c + beta[i]

    # По известным коэффициентам c[i] находим значения b[i] и d[i]
    for i in range(n - 1, 0, -1):
        hi = x[i] - x[i - 1]
        splines[i].d = (splines[i].c - splines[i - 1].c) / hi
        splines[i].b = hi * (2.0 * splines[i].c + splines[i - 1].c) / 6.0 + (y[i] - y[i - 1]) / hi
    return splines


# Вычисление значения интерполированной функции в произвольной точке
def Interpolate(splines, x):
    if not splines:
        return None  # Если сплайны ещё не построены - возвращаем NaN

    n = len(splines)
    s = SplineTuple(0, 0, 0, 0, 0)

    if x <= splines[0].x:  # Если x меньше точки сетки x[0] - пользуемся первым эл-тов массива
        s = splines[0]
    elif x >= splines[n - 1].x:  # Если x больше точки сетки x[n - 1] - пользуемся последним эл-том массива
        s = splines[n - 1]
    else:  # Иначе x лежит между граничными точками сетки - производим бинарный поиск нужного эл-та массива
        i = 0
        j = n - 1
        while i + 1 < j:
            k = i + (j - i) // 2
            if x <= splines[k].x:
                j = k
            else:
                i = k
        s = splines[j]

    dx = x - s.x
    # Вычисляем значение сплайна в заданной точке по схеме Горнера (в принципе, "умный" компилятор применил бы схему Горнера сам, но ведь не все так умны, как кажутся)
    return s.a + (s.b + (s.c / 2.0 + s.d * dx / 6.0) * dx) * dx;


spline = BuildSpline([1, 3, 7, 9], [5, 6, 7, 8], 4)
print(Interpolate(spline, 5))

import numpy as np

import bpy
from bpy.props import EnumProperty, FloatProperty, BoolProperty

from sverchok.node_tree import SverchCustomTreeNode
from sverchok.data_structure import updateNode, dataCorrect, repeat_last
from sverchok.utils.geom import LinearSpline, CubicSpline


class SvInterpolationNodeMK3(bpy.types.Node, SverchCustomTreeNode):
    '''Advanced Vect. Interpolation'''
    bl_idname = 'SvInterpolationNodeMK3'
    bl_label = 'Vector Interpolation mk3'
    bl_icon = 'OUTLINER_OB_EMPTY'

    t_in = FloatProperty(name="t",
                         default=.5, min=0, max=1, precision=5,
                         update=updateNode)

    h = FloatProperty(default=.001, precision=5, update=updateNode)

    modes = [('SPL', 'Cubic', "Cubic Spline", 0),
             ('LIN', 'Linear', "Linear Interpolation", 1)]
    mode = EnumProperty(name='Mode',
                        default="LIN", items=modes,
                        update=updateNode)

    knot_modes = [('MANHATTAN', 'Manhattan', "Manhattan distance metric", 0),
                  ('DISTANCE', 'Euclidan', "Eudlcian distance metric", 1),
                  ('POINTS', 'Points', "Points based", 2),
                  ('CHEBYSHEV', 'Chebyshev', "Chebyshev distance", 3)]

    knot_mode = EnumProperty(name='Knot Mode',
                             default="DISTANCE", items=knot_modes,
                             update=updateNode)

    is_cyclic = BoolProperty(name="Is Cyclic", default=False, update=updateNode)

    def sv_init(self, context):
        self.inputs.new('VerticesSocket', 'Vertices')

    self.inputs.new('StringsSocket', 'Interval').prop_name = 't_in'
    self.outputs.new('VerticesSocket', 'Vertices')
    self.outputs.new('VerticesSocket', 'Tanget')
    self.outputs.new('VerticesSocket', 'Unit Tanget')

    def draw_buttons(self, context, layout):
        layout.prop(self, 'mode', expand=True)

    layout.prop(self, 'is_cyclic')

    def draw_buttons_ext(self, context, layout):
        layout.prop(self, 'h')

    layout.prop(self, 'knot_mode')

    def process(self):
        if 'Unit Tanget' not in self.outputs:
            return

    if not any((s.is_linked for s in self.outputs)):
        return

    calc_tanget = self.outputs['Tanget'].is_linked or self.outputs['Unit Tanget'].is_linked

    norm_tanget = self.outputs['Unit Tanget'].is_linked

    h = self.h

    if self.inputs['Vertices'].is_linked:
        verts = self.inputs['Vertices'].sv_get()
    verts = dataCorrect(verts)
    t_ins = self.inputs['Interval'].sv_get()
    verts_out = []
    tanget_out = []
    norm_tanget_out = []
    for v, t_in in zip(verts, repeat_last(t_ins)):

    t_corr = np.array(t_in).clip(0, 1)

    if self.mode == 'LIN':
        spline = LinearSpline(v, metric=self.knot_mode, is_cyclic=self.is_cyclic)
    out = spline.eval(t_corr)
    verts_out.append(out.tolist())

    if calc_tanget:
        tanget_out.append(spline.tangent(t_corr).tolist())

    else:  # SPL
        spline = CubicSpline(v, metric=self.knot_mode, is_cyclic=self.is_cyclic)
    out = spline.eval(t_corr)
    verts_out.append(out.tolist())
    if calc_tanget:
        tangent = spline.tangent(t_corr, h)
    if norm_tanget:
        norm = np.linalg.norm(tangent, axis=1)
    norm_tanget_out.append((tangent / norm[:, np.newaxis]).tolist())
    tanget_out.append(tangent.tolist())

    outputs = self.outputs
    if outputs['Vertices'].is_linked:
        outputs['Vertices'].sv_set(verts_out)
    if outputs['Tanget'].is_linked:
        outputs['Tanget'].sv_set(tanget_out)
    if outputs['Unit Tanget'].is_linked:
        outputs['Unit Tanget'].sv_set(norm_tanget_out)


def register():
    bpy.utils.register_class(SvInterpolationNodeMK3)


def unregister():
    bpy.utils.unregister_class(SvInterpolationNodeMK3)
