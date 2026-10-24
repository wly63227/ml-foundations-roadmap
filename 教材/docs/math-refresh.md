# 数学唤醒手册

> 编者补充。先做自测，再只读遗忘部分。不是高数、线代和概率论的完整重讲。

<a id="linear"></a>

## 线性代数：先检查形状

把 $n$ 个观测、每个 $d$ 个特征按行放进 $X\in\mathbb R^{n\times d}$。参数 $w\in\mathbb R^d$，观测 $y\in\mathbb R^n$。于是预测 $Xw$ 与残差 $r=Xw-y$ 都在 $\mathbb R^n$。

内积 $a^Tb$ 把两个同维向量变成标量；二范数 $\|a\|_2=\sqrt{a^Ta}$ 衡量长度。矩阵乘法与逐元素相乘不是同一操作：NumPy 中分别是 `@` 与 `*`。

以荷载 $x_i$ 和位移 $y_i$ 的近似线性关系为例，设 $y_i\approx b+kx_i$。这只是局部示意模型。取 $X$ 的第 1 列为 1，第 2 列为荷载，$w=(b,k)^T$。最小化平方残差：

$$L(w)=\frac12(Xw-y)^T(Xw-y).$$

令梯度为零得正规方程 $X^TXw=X^Ty$。当 $X$ 列满秩时，$X^TX$ 正定且可逆，最小解唯一。若列相关，不能写逆矩阵；数值上使用 `np.linalg.lstsq` 或 SVD，通常比显式计算逆稳定。

向非零 $u\in\mathbb R^d$ 张成直线的投影为 $\hat y=u(u^Ty)/(u^Tu)$。残差满足 $u^T(y-\hat y)=0$。例如 $u=(1,1)^T,y=(2,1)^T$ 时投影为 $(1.5,1.5)^T$。

对任意实矩阵 $X$，SVD 写成 $X=U\Sigma V^T$；完整形式中 $U$ 为 $n\times n$，$\Sigma$ 为 $n\times d$，$V$ 为 $d\times d$。非零奇异值个数等于秩。PCA 在中心化数据上找方差最大的正交方向；特征单位和缩放会影响结果。

<a id="calculus"></a>

## 微积分：从变化率到梯度

标量函数 $f:\mathbb R^d\to\mathbb R$ 的梯度 $\nabla f\in\mathbb R^d$ 收集各偏导。若二阶连续可微，Hessian 是 $d\times d$ 的二阶偏导矩阵。向量函数 $g:\mathbb R^d\to\mathbb R^m$ 的 Jacobian 是 $m\times d$。不要把三者当成同一个对象。

对上述平方残差，逐项求导更容易看清维度：

$$L=\frac12\sum_{i=1}^n\left(\sum_{j=1}^dX_{ij}w_j-y_i\right)^2,$$
$$\frac{\partial L}{\partial w_k}=\sum_{i=1}^n(Xw-y)_iX_{ik},\qquad \nabla L=X^T(Xw-y).$$

若损失按样本平均，则梯度也除以 $n$。$\log x$ 只在 $x>0$ 使用，默认自然对数；链式法则要逐层追踪输入输出。

在可微点附近，$f(w+\Delta w)=f(w)+\nabla f(w)^T\Delta w+o(\|\Delta w\|)$。取 $\Delta w=-\eta\nabla f(w)$，一阶变化为 $-\eta\|\nabla f(w)\|^2$。这解释了非零梯度、小步长时的局部下降；不能保证任意学习率都下降。

有限差分用于检查实现：第 $k$ 个分量近似 $[L(w+\epsilon e_k)-L(w-\epsilon e_k)]/(2\epsilon)$。用双精度和如 $10^{-6}$ 的扰动检查光滑小例子，避免在 ReLU 的不可微点判定梯度错误。凸函数的驻点是全局最小点；一般非凸函数不具备这个保证。

<a id="probability"></a>

## 概率：把条件写完整

当 $P(B)>0$ 时，$P(A\mid B)=P(B\mid A)P(A)/P(B)$。分母需要全概率公式，不能直接把检测准确率当作后验。

离散概率质量与连续密度不同：连续情形中 $P(a\le X\le b)=\int_a^bp(x)\,dx$。密度非负、总积分为 1，可以大于 1。存在密度时，单点概率为 0。期望和方差的讨论需要相应矩存在；方差有限时 $\operatorname{Var}(X)=E[X^2]-E[X]^2$。

随机向量 $Z\in\mathbb R^d$ 的协方差矩阵为 $E[(Z-\mu)(Z-\mu)^T]\in\mathbb R^{d\times d}$，其中二阶矩有限。独立能推出不相关（相应矩存在时）；反方向通常不成立。

独立同分布 Bernoulli 样本 $x_i\in\{0,1\}$，记 $s=\sum_i x_i$，似然为：

$$L(\theta)=\theta^s(1-\theta)^{n-s},\quad 0\le\theta\le1.$$

观测固定，似然是参数的函数，并非关于参数归一化的密度。在 $0<\theta<1$ 上求对数与导数：

$$\ell=s\log\theta+(n-s)\log(1-\theta),\quad \ell'=\frac{s}{\theta}-\frac{n-s}{1-\theta}.$$

当 $0<s<n$，解为 $\hat\theta=s/n$；全 0 或全 1 的最大值在边界，应直接比较似然而非代入无定义的对数。

先验 Beta($\alpha,\beta$)，$\alpha,\beta>0$，后验为 Beta($\alpha+s,\beta+n-s$)。两参数均大于 1 时，后验众数为 $(\alpha+s-1)/(\alpha+\beta+n-2)$，这才是内部 MAP 公式。后验均值为 $(\alpha+s)/(\alpha+\beta+n)$，二者不能混用。

<a id="new-topics"></a>

## 统计与优化：哪些需要新补

- 梯度下降最小化指定目标；目标值下降不等于测试误差下降。
- MLE 只用似然；MAP 加入先验。某些先验可对应正则项，但需逐个模型说明。
- 大数定律描述样本均值在条件下接近期望；中心极限定理描述适当标准化后的均值分布，不是说原始数据会变正态。
- 第 9 周重点学习数据划分、交叉验证和泄漏；统计检验与区间估计留作进一步学习。

手算题见 [自测](diagnostic.md)，推导核对见 [参考解](answers.md)，实验命令见 [环境准备](setup.md)。
