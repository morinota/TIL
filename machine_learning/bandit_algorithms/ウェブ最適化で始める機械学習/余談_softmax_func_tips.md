## 余談: ソフトマックス関数のオーバーフローを回避するためのtips


### 最大値を引く方法

- tips
  - ロジット値をそのままexp()に入れると巨大な値になりオーバーフローを起こす可能性がある。回避するために、ここではロジット値の最大値を引いてからexp()に入れる。
- 利点
  - 値のオーバーフロー回避。
  - 値のアンダーフロー回避。
  - 数値的な安定性: 
  - 結果の不変性：**実は最大値を引いても、ソフトマックス関数の出力は変わらない**。これは、ソフトマックス関数の性質によるもの。


### pytorch.softmax()について

2つの方法がある
- `torch.nn.functional.softmax()`
- `torch.nn.Softmax()`
  
前者の例

```python
import torch
import torch.nn.functional as F

input = torch.tensor([[1.0, 2.0, 3.0], [4.0, 5.0, 6.0]])

output = F.softmax(input, dim=1)

print(output)
# tensor([[0.0900, 0.2447, 0.6652],
#         [0.0900, 0.2447, 0.6652]])
```

後者の例

```python
import torch.nn as nn
softmax = nn.Softmax(dim=-1)
output = softmax(input)
```

**ただし温度パラメータを指定できない点に注意! 任意の温度パラメータを指定させたい場合は、自前で実装する必要がある**。
ただまあ、logit値のリストを渡す際に、温度パラメータの値で割った状態で`torch.softmax()`に渡せばそれでOK!

ex.

```python
import torch
import torch.nn.functional as F

def temp_softmax(x, temperature=1.0):
    return F.softmax(x / temperature, dim=-1)
```
