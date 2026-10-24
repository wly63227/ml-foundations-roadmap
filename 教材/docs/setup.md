# 环境准备与可运行实验

## 第一个程序：暂时只需要 Python

安装 Python 3.12 后，在终端执行 `python --version`。Windows 若跳转应用商店，先确认实际安装的解释器路径，不要反复双击 `.py` 文件。可以用 VS Code 或任意文本编辑器写文件；保存为 `hello.py`，内容如下：

```python
readings = [1.0, 1.2, 0.8]
mean = sum(readings) / len(readings)
print("平均读数:", mean)
```

终端进入文件所在目录，执行 `python hello.py`，应输出均值 1.0。`=` 是赋值，`==` 才是比较；缩进划定循环和函数体。先预测输出，再运行，再改一个数重跑。

## 独立环境

以下命令都在仓库根目录执行。Python 3.12 为已选验证环境，不要求 GPU。前三周先用科学计算依赖，PyTorch 到第 11 周再安装。

```powershell
python -m venv .venv
.venv/Scripts/python.exe -m pip install -r requirements-ml.txt
.venv/Scripts/python.exe -m pip install -r requirements-torch.txt
```

macOS/Linux 改用 `.venv/bin/python`。这里顶层学习依赖固定版本；间接依赖由 pip 解析，尚不等于完整跨平台环境锁。遇到版本问题先保留错误与 `pip freeze`，不要盲目全局升级。

## 实验入口

本仓库的 `教材/scripts/examples.py` 全部为自编教学示例。先运行，再遮住代码重写核心部分。运行成功不等于已经掌握。

| 命令尾部 | 依赖 | 对应周与输出 |
| --- | --- | --- |
| `basics` | 标准库 | 1–2：CSV 往返、均值和样本数 |
| `arrays` | NumPy、Matplotlib | 3：轴均值、广播、测量图 SVG |
| `linear` | NumPy | 4、7：最小二乘、梯度下降与拟合误差 |
| `gradient` | NumPy | 5：解析梯度与有限差分误差 |
| `probability` | NumPy | 6：后验、MLE、MAP 与重复采样 |
| `logistic` | NumPy | 8：稳定交叉熵、正则化与梯度核对 |
| `evaluation` | scikit-learn | 9–10、15：划分、交叉验证、基线、树、PCA、聚类 |
| `autograd` | CPU PyTorch | 11–12：手算梯度与训练循环 |
| `neural` | CPU PyTorch、scikit-learn | 13–16：MLP、验证集曲线、CNN 形状 |
| `all` | 全部 | 逐个运行并写实验报告 JSON |

例如：

```powershell
.venv/Scripts/python.exe 教材/scripts/examples.py gradient
.venv/Scripts/python.exe 教材/scripts/verify_math.py
```

生成文件写入 `教材/reports/`，不纳入 Git；学习者应在自己的学习记录中写观察和解释。实验默认固定种子 42；代码内部设定 CPU 和少量线程，小型合成数据无需外部下载。

## 常见错误与排查顺序

- `ModuleNotFoundError`：确认安装依赖与运行脚本使用同一个 Python。
- 维度不匹配：先打印 `.shape`，逐个检查轴，再考虑 reshape，不要靠试错强行拼接。
- 数值为 `nan`：检查输入、学习率和对数条件；逻辑回归使用稳定的 `logaddexp`。
- loss 不变：检查梯度、更新语句和是否每次意外重置参数。
- Git 操作：先 `git status`、`git diff`，只暂存明确修改过的文件；不要用 reset 清理不认识的改动。

## 网站本地构建

网站依赖 Node.js 22 和 pnpm 10。执行 `pnpm install --frozen-lockfile`、`pnpm build`、`pnpm check`。再执行 `python -m http.server 8766 --bind 127.0.0.1 --directory 教材/site`，浏览器打开 `http://127.0.0.1:8766/`。正文和公式为静态 HTML；数学字体本地提供，加载后不需要远端数学服务。
