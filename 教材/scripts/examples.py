"""自编 CPU 教学实验；从仓库任意目录启动，输出统一写入 reports。

运行成功只代表实现检查，不代表学习者掌握。默认不展示测试集指标；
冻结方案后才用 --final。每个函数可作为遮住答案后重写的小任务。
"""
import argparse
import csv
import json
import math
import os
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'reports'
OUT.mkdir(exist_ok=True)
os.environ.setdefault('MPLCONFIGDIR', str(OUT / '.matplotlib'))


def basics():
    values = [1.0, 1.2, 0.8]
    with (OUT / 'readings.csv').open('w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['reading_mm'])
        writer.writerows([[v] for v in values])
    with (OUT / 'readings.csv').open(encoding='utf-8') as f:
        loaded = [float(row['reading_mm']) for row in csv.DictReader(f)]
    def mean(data):
        if not data:
            raise ValueError('Cannot average an empty sequence')
        return sum(data) / len(data)
    assert loaded == values and math.isclose(mean(loaded), 1.0)
    try:
        mean([])
    except ValueError:
        pass
    else:
        raise AssertionError('Empty data must be rejected')
    return {'count': len(loaded), 'mean_mm': mean(loaded), 'mse_vs_1': sum((v-1)**2 for v in loaded)/3}


def arrays():
    import numpy as np
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    x = np.array([[1., 2.], [3., 4.], [5., 6.]])
    shifted = x + np.array([10., 20.])
    product = x @ np.array([1., -1.])
    assert np.allclose(x.mean(axis=0), [3, 4])
    assert shifted.shape == (3, 2) and np.allclose(product, [-1, -1, -1])
    load = np.array([0., 1., 2., 3.])
    displacement = np.array([0.05, 0.95, 2.10, 3.00])
    fig, ax = plt.subplots(figsize=(5, 3.3), layout='constrained')
    ax.scatter(load, displacement, color='#1b624c')
    ax.set(xlabel='Synthetic load (kN)', ylabel='Synthetic displacement (mm)', title='Teaching data, not field measurements')
    fig.savefig(OUT / 'measurements.svg')
    plt.close(fig)
    return {'shape': list(x.shape), 'column_mean': x.mean(axis=0).tolist(), 'broadcast': shifted.tolist(), 'product': product.tolist()}


def central_difference(fun, w, eps=1e-6):
    import numpy as np
    result = np.empty_like(w, dtype=float)
    for j in range(len(w)):
        delta = np.zeros_like(w, dtype=float)
        delta[j] = eps
        result[j] = (fun(w+delta)-fun(w-delta))/(2*eps)
    return result


def linear():
    import numpy as np
    x = np.array([0., 1., 2.])
    X = np.column_stack([np.ones(3), x])  # X: (n=3,d=2); w: (2,); y: (3,)
    y = 1+2*x
    exact, _, rank, _ = np.linalg.lstsq(X, y, rcond=None)
    w = np.zeros(2)
    history = []
    for _ in range(3000):
        residual = X@w-y
        history.append(float(residual@residual/(2*len(y))))
        w -= 0.05*(X.T@residual)/len(y)
    assert np.allclose(exact, [1., 2.]) and np.allclose(w, exact, atol=1e-7)
    assert history[-1] < history[0]
    singular = np.column_stack([x, x])
    assert np.linalg.matrix_rank(singular) == 1
    return {'X_shape': list(X.shape), 'rank': int(rank), 'lstsq': exact.tolist(), 'gradient_descent': w.tolist(), 'initial_loss': history[0], 'final_loss': history[-1], 'singular_rank': 1}


def gradient():
    import numpy as np
    X = np.array([[1., 0.], [1., 1.], [1., 2.]])
    y, w = np.array([1., 3., 5.]), np.array([.3, -.2])
    def loss(v):
        r = X@v-y
        return r@r/(2*len(y))
    analytic = X.T@(X@w-y)/len(y)
    numeric = central_difference(loss, w)
    error = float(np.max(np.abs(analytic-numeric)))
    assert error < 1e-6
    return {'analytic': analytic.tolist(), 'finite_difference': numeric.tolist(), 'max_absolute_error': error}


def probability():
    import numpy as np
    posterior = (.01*.9)/(.01*.9+.99*.1)
    rng = np.random.default_rng(42)
    # Compare variation over repeated sample means, not monotone error of one run.
    means_small = rng.binomial(10, .6, size=2000)/10
    means_large = rng.binomial(1000, .6, size=2000)/1000
    assert np.isclose(posterior, 1/12)
    assert means_large.std() < means_small.std()
    assert abs(means_large.mean()-.6) < .01
    return {'posterior_abnormal_given_positive': posterior, 'mle': 2/3, 'map_beta22': 3/5, 'posterior_mean': 4/7, 'sd_mean_n10': float(means_small.std()), 'sd_mean_n1000': float(means_large.std())}


def logistic():
    import numpy as np
    rng = np.random.default_rng(42)
    features = rng.normal(size=(200, 2))
    X = np.column_stack([np.ones(len(features)), features])
    y = (1.5*features[:, 0]-features[:, 1]+.3*rng.normal(size=200)>0).astype(float)
    strength = .02
    def loss(w):
        z = X@w
        # log(1+exp(z)) - yz, stable even for large |z|.
        return np.mean(np.logaddexp(0, z)-y*z)+strength*(w[1:]@w[1:])/2
    def grad(w):
        p = np.exp(-np.logaddexp(0, -(X@w)))
        penalty = strength*w.copy()
        penalty[0] = 0  # Do not regularize the intercept.
        return X.T@(p-y)/len(y)+penalty
    trial = np.array([.2, -.1, .3])
    error = float(np.max(np.abs(grad(trial)-central_difference(loss, trial))))
    assert error < 1e-6
    w = np.zeros(3)
    initial = float(loss(w))
    for _ in range(1200):
        w -= .1*grad(w)
    assert loss(w) < initial and np.isfinite(loss(w))
    return {'gradient_check_error': error, 'initial_loss': initial, 'final_loss': float(loss(w)), 'weights_including_intercept': w.tolist(), 'note': 'Training-only demonstration; not an independent accuracy estimate.'}


def project_data():
    """Shared generated data and identical indices for classical and neural models."""
    import numpy as np
    from sklearn.model_selection import train_test_split
    rng = np.random.default_rng(42)
    X = rng.normal(size=(600, 4))
    y = 2*X[:, 0]-X[:, 1]+.7*np.sin(2*X[:, 2])+rng.normal(0, .15, 600)
    trainval, test = train_test_split(np.arange(600), test_size=.2, random_state=42)
    train, val = train_test_split(trainval, test_size=.25, random_state=43)
    assert len(set(train)&set(val)) == len(set(train)&set(test)) == len(set(val)&set(test)) == 0
    return X, y, train, val, test


def evaluation(final=False):
    import numpy as np
    from sklearn.cluster import KMeans
    from sklearn.decomposition import PCA
    from sklearn.dummy import DummyRegressor
    from sklearn.linear_model import Ridge
    from sklearn.metrics import mean_squared_error
    from sklearn.model_selection import KFold, cross_val_score
    from sklearn.pipeline import make_pipeline
    from sklearn.preprocessing import StandardScaler
    from sklearn.tree import DecisionTreeRegressor
    X, y, train, val, test = project_data()
    models = {'mean': DummyRegressor(), 'ridge': make_pipeline(StandardScaler(), Ridge(alpha=1.)), 'tree_depth3': DecisionTreeRegressor(max_depth=3, random_state=42)}
    result = {'split_counts': [len(train), len(val), len(test)], 'seed': 42, 'metric': 'MSE', 'models': {}}
    splitter = KFold(n_splits=3, shuffle=True, random_state=42)
    for name, model in models.items():
        # cross_val_score clones the whole Pipeline, fitting each scaler only on that fold.
        cv = -cross_val_score(model, X[train], y[train], scoring='neg_mean_squared_error', cv=splitter)
        model.fit(X[train], y[train])
        pred = model.predict(X[val])
        entry = {'cv_mse_mean': float(cv.mean()), 'cv_mse_std': float(cv.std()), 'validation_mse': float(mean_squared_error(y[val], pred))}
        if final:
            entry['test_mse'] = float(mean_squared_error(y[test], model.predict(X[test])))
        result['models'][name] = entry
    assert result['models']['ridge']['validation_mse'] < result['models']['mean']['validation_mse']
    pca = make_pipeline(StandardScaler(), PCA(n_components=2)).fit(X[train])
    projected = pca.transform(X[val])
    assert projected.shape == (120, 2)
    clusters = make_pipeline(StandardScaler(), KMeans(n_clusters=3, n_init=10, random_state=42)).fit(X[train])
    assert len(clusters.predict(X[val])) == 120
    result['pca_explained_variance_ratio'] = pca[-1].explained_variance_ratio_.tolist()
    result['kmeans_training_inertia'] = float(clusters[-1].inertia_)
    return result


def autograd():
    import torch
    torch.manual_seed(42)
    torch.set_num_threads(1)
    x = torch.tensor([1., 2.], dtype=torch.float64, requires_grad=True)
    (x*x).sum().backward()
    assert torch.allclose(x.grad, torch.tensor([2., 4.], dtype=torch.float64))
    first = x.grad.tolist()
    x.grad = None
    ((2*x+1)**2).sum().backward()
    assert torch.allclose(x.grad, torch.tensor([12., 20.], dtype=torch.float64))
    X = torch.tensor([[0.], [1.], [2.]], dtype=torch.float64)
    y = 1+2*X
    model = torch.nn.Linear(1, 1).double()
    optimizer = torch.optim.SGD(model.parameters(), lr=.05)
    initial = float(torch.nn.functional.mse_loss(model(X), y).detach())
    model.train()
    for _ in range(1500):
        prediction = model(X)
        loss = torch.nn.functional.mse_loss(prediction, y)
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()
    model.eval()
    with torch.no_grad():
        final_loss = float(torch.nn.functional.mse_loss(model(X), y))
    assert final_loss < 1e-10
    return {'gradient_square': first, 'gradient_composite': x.grad.tolist(), 'initial_mse': initial, 'final_mse': final_loss, 'slope': float(model.weight.detach()[0, 0]), 'intercept': float(model.bias.detach()[0])}


def neural(final=False):
    import numpy as np
    import torch
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    from sklearn.preprocessing import StandardScaler
    torch.manual_seed(42)
    torch.set_num_threads(1)
    X, y, train, val, test = project_data()
    scaler = StandardScaler().fit(X[train])
    xt = torch.tensor(scaler.transform(X[train]), dtype=torch.float32)
    yt = torch.tensor(y[train, None], dtype=torch.float32)
    xv = torch.tensor(scaler.transform(X[val]), dtype=torch.float32)
    yv = torch.tensor(y[val, None], dtype=torch.float32)
    model = torch.nn.Sequential(torch.nn.Linear(4, 16), torch.nn.ReLU(), torch.nn.Linear(16, 1))
    optimizer = torch.optim.Adam(model.parameters(), lr=.01, weight_decay=1e-4)
    history = []
    # Fixed schedule for the reference implementation. Learner changes use validation only.
    for epoch in range(200):
        model.train()
        permutation = torch.randperm(len(xt))
        for batch in permutation.split(60):
            loss = torch.nn.functional.mse_loss(model(xt[batch]), yt[batch])
            optimizer.zero_grad()
            loss.backward()
            optimizer.step()
        model.eval()
        with torch.no_grad():
            history.append([float(torch.nn.functional.mse_loss(model(xt), yt)), float(torch.nn.functional.mse_loss(model(xv), yv))])
    assert np.isfinite(history).all() and history[-1][0] < history[0][0]
    result = {'split_counts': [len(train), len(val), len(test)], 'hidden_width': 16, 'epochs': 200, 'batch_size': 60, 'learning_rate': .01, 'weight_decay': 1e-4, 'training_mse': history[-1][0], 'validation_mse': history[-1][1], 'device': 'cpu'}
    if final:
        with torch.no_grad():
            prediction = model(torch.tensor(scaler.transform(X[test]), dtype=torch.float32)).numpy().ravel()
        result['test_mse'] = float(np.mean((prediction-y[test])**2))
    fig, ax = plt.subplots(figsize=(5, 3.3), layout='constrained')
    ax.plot(np.array(history)[:, 0], label='Train')
    ax.plot(np.array(history)[:, 1], label='Validation')
    ax.set(xlabel='Epoch', ylabel='MSE', title='Synthetic regression, CPU MLP')
    ax.legend()
    fig.savefig(OUT/'mlp-learning.svg')
    plt.close(fig)
    conv = torch.nn.Conv2d(1, 4, kernel_size=3, padding=1)
    shape = list(conv(torch.zeros(2, 1, 8, 8)).shape)
    count = sum(p.numel() for p in conv.parameters())
    assert shape == [2, 4, 8, 8] and count == 40
    result.update(cnn_shape=shape, cnn_parameters=count)
    return result


COMMANDS = {'basics': basics, 'arrays': arrays, 'linear': linear, 'gradient': gradient, 'probability': probability, 'logistic': logistic, 'evaluation': evaluation, 'autograd': autograd, 'neural': neural}
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('command', choices=['all', *COMMANDS])
    parser.add_argument('--final', action='store_true', help='Only after freezing choices: include held-out test MSE.')
    args = parser.parse_args()
    selected = COMMANDS if args.command == 'all' else {args.command: COMMANDS[args.command]}
    report = {}
    for name, fun in selected.items():
        report[name] = fun(final=args.final) if name in ('evaluation', 'neural') else fun()
        print(name, json.dumps(report[name], ensure_ascii=False))
    filename = f'examples-{args.command}{"-final" if args.final else ""}.json'
    (OUT/filename).write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding='utf-8')
