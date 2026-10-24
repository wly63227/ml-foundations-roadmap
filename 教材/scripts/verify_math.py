"""核算自测与周练的数值；不把数值核算当作全部数学证明。"""
import json
from datetime import datetime, timezone
from pathlib import Path
import numpy as np

checks = []
def check(name, actual, expected, atol=1e-9):
    passed = bool(np.allclose(actual, expected, atol=atol, rtol=1e-9))
    checks.append({'name': name, 'passed': passed})
    if not passed:
        raise AssertionError(f'{name}: {actual} != {expected}')

X = np.array([[1., 0.], [1., 1.], [1., 2.]])
check('A1 residual and gradient dimensions', [(X@np.zeros(2)).size, (X.T@np.zeros(3)).size], [3, 2])
a, b = np.array([1., 2.]), np.array([2., -1.])
check('A2 dot and norm', [a@b, np.linalg.norm(a)], [0, np.sqrt(5)])
A = np.array([[1., 2.], [2., 4.]])
check('A3 rank determinant', [np.linalg.matrix_rank(A), np.linalg.det(A)], [1, 0])
u, y = np.array([1., 1.]), np.array([2., 1.])
projection = u*(u@y)/(u@u)
check('A4 projection', projection, [1.5, 1.5])
check('A4 orthogonal residual', u@(y-projection), 0)
check('A5 eigenvalues', np.linalg.eigvalsh(np.diag([2., 3.])), [2, 3])
check('B6 log derivative numerical', (np.log(1+(1+1e-6)**2)-np.log(1+(1-1e-6)**2))/2e-6, 1, atol=1e-7)
check('B7 gradient', [4*(2*1+0-3), 2*(2*1+0-3)], [-4, -2])
check('B8 Taylor approximation', [1+2*.01, 1.01**2-(1+2*.01)], [1.02, .0001])
check('B9 gradient descent step', 0-.1*2*(0-3), .6)
w, target = np.array([.3, -.2]), np.array([1., 3., 5.])
g = X.T@(X@w-target)
eps = 1e-6
loss = lambda v: .5*np.sum((X@v-target)**2)
numeric = np.array([(loss(w+eps*np.eye(2)[j])-loss(w-eps*np.eye(2)[j]))/(2*eps) for j in range(2)])
check('B10 matrix gradient', g, numeric, atol=1e-6)
check('C11 posterior', .009/(.009+.099), 1/12)
check('C12 density integral and interval', [2*.5, 2*.1], [1, .2])
check('C13 moments', [np.mean([0., 2.]), np.var([0., 2.])], [1, 1])
grid = np.linspace(0, 1, 3001)
check('C14 MLE grid', grid[np.argmax(grid**2*(1-grid))], 2/3)
check('C15 MAP grid', grid[np.argmax(grid**3*(1-grid)**2)], 3/5)
check('C15 posterior mean', 4/(4+3), 4/7)
check('W01 shifted and filtered means', [np.mean([1., 1.2, .8])+.5, np.mean([1., 1.2])], [1.5, 1.1])
check('W02 MSE', np.mean((np.array([1., 1.2, .8])-1)**2), .08/3)
matrix = np.arange(1., 7.).reshape(3, 2)
check('W03 column means', matrix.mean(axis=0), [3, 4])
check('W03 broadcast', matrix+np.array([10, 20]), [[11, 22], [13, 24], [15, 26]])
check('W03 multiplication', matrix@np.array([1, -1]), [-1, -1, -1])
check('W04 and W07 least squares', np.linalg.lstsq(X, target, rcond=None)[0], [1, 2])
check('W08 sigmoid loss and gradient', [1/(1+np.exp(0)), np.logaddexp(0, 0), -.5, -1], [.5, np.log(2), -.5, -1])
check('W09 classification metrics', [14/20, 8/10, 8/12], [.7, .8, 2/3])
check('W10 cluster squared distances', np.sum(np.array([-2., 0., 2.])**2), 8)
check('W11 composite gradient', 4*(2*np.array([1., 2.])+1), [12, 20])
check('W12 update', [1-.1*(-6), 0-.1*(-3)], [1.6, .3])
check('W13 parameter count', 4*8+8+8+1, 49)
check('W14 CNN shape and parameters', [int((8+2-3)/1)+1, 4*1*3*3+4], [8, 40])
check('W15 split', [600*.6, 600*.2, 600*.2], [360, 120, 120])
check('W16 relative improvements', [1-.4/4, 1-.5/4], [.9, .875])
out = Path(__file__).resolve().parents[1]/'reports'
out.mkdir(exist_ok=True)
report = {'checkedAt': datetime.now(timezone.utc).isoformat(), 'checks': checks, 'passed': len(checks), 'failed': 0}
(out/'math.json').write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding='utf-8')
print(f'{len(checks)} numeric checks passed.')
