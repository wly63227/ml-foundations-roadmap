# 精选资源与阅读范围

## 选择原则

中文说明为主，英文用于补充。每模块只选一份主资源和至多一份可选补充。下列网页入口与主要目录在 2026-10-24 核查；不代表已逐段审校所有外链内容，也不保证未来地址和版本不变。不复制原书或课件，不虚构 PDF 页码。

<a id="python"></a>

## Python 与科学计算

主资源：先读本路线 [环境准备](setup.md) 和第 1–3 周中文说明，亲手运行代码，再查 [Python 3.12 中文教程](https://docs.python.org/zh-cn/3.12/tutorial/)。第 1 周只读第 3 章和第 4 章的 if、for、range；第 2 周读函数、数据结构、输入输出与异常。初学者不用一次读完整本语言文档。

可选补充：[NumPy 官方入门](https://numpy.org/doc/stable/user/absolute_beginners.html)。只读创建数组、形状、索引、基础运算和广播；英语术语对照：shape 形状、axis 轴、broadcasting 广播、view 视图。绘图先模仿本仓库例子，不要求读完 Matplotlib 文档。

<a id="math"></a>

## 数学复习

主资源：[数学唤醒手册](math-refresh.md)，按自测错题选读。高数、线代、概率分别仅安排一周。

可选补充：[Mathematics for Machine Learning 作者网站](https://mml-book.github.io/)。按需读第 2–4 章的线代、几何、分解，第 5 章的向量微积分，第 6 章的概率，第 7 章的连续优化。只读与错题对应的小节；不要求三周读完这些章节。作者提供合法在线版本，本仓库只给入口。

<a id="ml"></a>

## 经典机器学习

主资源：[已有中文机器学习教材](https://wly63227.github.io/UCAS-machine-learning/)。第 7 周看回归章最小二乘，第 8 周看线性分类的 logistic，第 9 周看评价，第 10 周看树、聚类、PCA 相应小节。该教材仍为初稿，不把其未审校内容视为已验收。

可选补充：[scikit-learn Getting Started](https://scikit-learn.org/stable/getting_started.html)。重点看 `fit/predict`、Pipeline、划分和交叉验证。读代码时先看数据形状和在哪个子集调用 fit。

<a id="dl"></a>

## 深度学习

主资源：[中文版《动手学深度学习》](https://zh.d2l.ai/)。第 11 周读 2.1、2.5；第 12 周读 3.2、4.7；第 13 周读 4.1–4.4；第 14 周读 4.5–4.6、6.2–6.3。使用 PyTorch 分支，先跑本仓库 CPU 小例子，不安装整套 d2l 依赖，避免其环境约束与本仓库混合。

可选补充：[PyTorch Learn the Basics](https://docs.pytorch.org/tutorials/beginner/basics/intro.html)。按 Tensor、Autograd、Optimization 的顺序查询。术语：gradient 梯度、batch 批、epoch 一轮训练、inference 推断。

## 外部资源记录

| 来源 ID | 类型与用途 | 核查范围 | 处理状态 |
| --- | --- | --- | --- |
| WEB-PY | Python 官方中文教程，语言查阅 | 教程入口及章节目录 | 入口核查；未逐段审校 |
| WEB-NP | NumPy 官方资源，数组补充 | 官方 Learn 页及入门入口 | 入口核查；未逐段审校 |
| WEB-MML | 作者官网，数学补充 | 作者网站及章节目录 | 目录核查；未使用 PDF 页码 |
| WEB-D2L | 作者中文教材，深度学习主线 | 预备知识与后续章节目录 | 目录核查；未逐段审校 |
| WEB-SK | scikit-learn 官方指南 | Getting Started 的划分与 Pipeline 示例 | 页面核查；本仓库代码另行验证 |
| WEB-TORCH | PyTorch 官方教程 | 基础教程目录 | 入口核查；本仓库代码另行验证 |
| LOCAL-COURSE | 现有课程教材网站 | 本地既有章节结构 | 保留原有初稿审校边界 |

本版没有新增或处理原始 PDF，因此没有 PDF 哈希或物理逐页记录；以后引入 PDF 时必须单独建立，不能把本表当成逐页验收。
