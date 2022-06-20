---
marp: true
theme: gaia
_class: lead
paginate: true
backgroundColor: #fff
backgroundImage: url('https://marp.app/assets/hero-background.svg')
header: Matrix Factrization
footer: 2022, 5, 17 Morita
style: |
  section.title * , h1{
      text-align: center;
  }
---

<!-- ![bg left:50% 80%](因果ダイアグラム.drawio.png) -->

![bg 50% opacity:.3](因果ダイアグラム.drawio.png)

# **Idea of Personalized Recommendation**

### 推薦システムのアイデア

### 

回帰分析を通して因果関係を議論したい時に注意すべきこと

2022/05/08 Whole seminar
Masato MORITA

---

# First of all, **Why I chose this topic**??

### 1. I have the impression that more and more members are using regression analysis in their research activities these days.

### 2. I recently read a book on statistical causal inference and learned how to analyze causality using regression analysis, so I want to share some information a little bit...!

---

# Today's My Objective

I want to share one of the idea of **Statistical Causal Inference (統計的因果推論)**: it is the field of analysing causal relation from observed dataset.

#### (Dear user of regression analysis)

###### I want to share **what we should careful when interpreting the value of regression coefficient** from viewpoint of causal inference.

#### (Dear not user of regression analysis)
###### I want to share **the patterns that may mislead us** when discussing causal relation based on observed data.

---

# Outline

### 1. What is causal relation? What is regression analysis?

因果関係ってなんだっけ？回帰分析ってなんだっけ？

### 2. When is **regression coefficients** different from **causal effects**? 

どんな場合に回帰係数の値と因果効果の値がズレる？

---

<!-- _class: title -->

# 1. What is causal relation? What is regression analysis?

因果関係ってなんだっけ？回帰分析ってなんだっけ？

---

# What is Causal Relation?
#### - The definition of causal relation is ...
###### In case that **"when factor X is changed (intervention), factor Y also changes,"** we can say "there is a **causal relationship of factor X → factor Y**
  
- The difference with correlation is ...
  ![w: h:9cm](relations_3kinds.png)

---

# What is Causal Effect?
#### - The definition of causal relation is ...
###### In case that **"when factor X is changed (intervention), factor Y also changes**," we can say "there is a **causal relationship of factor X → factor Y**
  
In above case,
##### - X: "cause"(原因変数), Y: "outcome"(結果変数)
##### - "**causal effect(intervention effect)** of $X \Rightarrow Y$" :Average change of Y when X is changed by one unit

#### In Causal Inference, one motivation is quontification of causal effect.
---
# What is Linear Regression Analysis?

It's a little bit mathematical.

$$
\mathbf{y} = f(\mathbf{x_1}, \cdots, \mathbf{x}_k) + \mathbf{\epsilon}\\
= \beta_0 + \beta_1 \mathbf{x}_1 + \cdots + \beta_k \mathbf{x}_k + \mathbf{\epsilon}
= \mathbf{\beta}X + \mathbf{\epsilon}
$$

where is ...

###### $\mathbf{y}$ : (in Causal Inference, it should be "outcome")
###### $X$ : (in Causal Inference, it should include "cause")
###### $\mathbf{\beta}$ : the regression coefficent of $X$.
###### $\mathbf{\epsilon}$ : Probabilistic component of y。

---

# the usage of Regression analysis

the usage of Regession analysis is separated mainly three objectives:

![w: h:8cm](objectives_of_regression_analysis.png)

from viewpoint of "Causal Inference", regression analysis is utilized for "Description" and "Control/Intervention".

---

# Example: height=>weight

$$
\text{weight} = \beta_0 + \beta_1 \times \text{height} + \epsilon \\
\Rightarrow \beta_1 = 0.34 (p = 0.00)
$$

###### In this case, $\beta_1$ can be interpret 'causal effect' of 'height' $\Rightarrow$ 'weight'.

###### However, the value of the regression coefficient **does not necessarily fit** with the causal effect.

![bg left:50% 90%](height_x_weight_y_with_LRline.png)

---

# 2. When is **regression coefficients** different from **causal effects**?

there are mainly 4 cases :

### 1. Direction of causation is opposite

### 2. **Confounding**

### 3. Selection Bias

### 4. Intermediate variables are included

---

# Let's imagine the case of saving Biodiversity

<!-- 河川の生物多様性の保全の為に、私達は「生物の種数」と河川中の環境汚染物質について調査する事にした。 -->

#### For preserving biodiversity of the river, we decided to investigate the "biodiversity in the river(num of species)" and some kind of "environmental pollutants" in the river.

---

### A negative linear correlation was found between the "biodiversity in the river" and "zinc concentration(亜鉛濃度)".

![bg left:35% 100%](Zinc_x_Biodiversity_y.png)

###### At this point, taking into account the general finding that "high zinc concentration is toxic to many organisms,"

###### we can guess easily the causal relationship of "**increased zinc concentration in the river"(X) => "decreased biodiversity in the river"(Y)**.

---

![bg left:35% 100%](Zinc_x_Biodiversity_y_with_line.png)
### Let's quantify causal effect by regression analysis

###### Let's analyze the "biodiversity in the river" using a single regression model with "zinc concentration" as the explanatory variable.

$$
\text{biodiversity}  = \beta_0 + \beta_1 \times \text{zinc concentration} + \epsilon
$$

###### we estimated the regression coefficient $\beta_1= -0.87(p=0.00)$

###### So we can say $\beta_1= -0.87$ is **the causal effect of "zinc concentration" to "biodiversity**"??

---

---

# So we can guess this causal relation

![bg 60% opacity:1.0](因果ダイアグラム_1.drawio.png)

---

# However...

![bg left:35% 100%](BOD_x_Biodiversity_y.png)

###### Further investigation revealed that ....

- a negative linear correlation between "biodiversity in the river" and "BOD in the river" is also observed.

- Therefore, we cas also guess a causal relationship of "increase in BOD" => "decrease biodiversity"...

---

# However...

![bg left:35% 100%](BOD_x_Biodiversity_y_with_LRline.png)

###### Let's try regression analysis...

$$
\text{biodiversity}  = \beta_0 + \beta_2 \times \text{BOD} + \epsilon
$$

###### we estimated the regression coefficient $\beta_2= -1.81(p=0.00)$

<!-- ここで果たして、「亜鉛が河川生物の種数を減らしている」と言えるのか？ -->

#### In this case, **can we really say that "zinc concentration is reducing the biodiversity in the river?**"

---
# In actual...There is "Confounding"

![bg 40% opacity:1.0](因果ダイアグラム_2.drawio.png)

 <!-- So truth causal effect of zinc concentration to biodiversity is close to 0.0. -->
---

# Let's check confounding using regression analysis

###### in this case, one way is **a multiple regression analysis** with "biodiversity in the river" as the exprained variable and "zinc concentration" and "BOD" as the explanatory variables.

$$
\text{biodiversity in the river} = \beta_0 + \beta_1 \times \text{zinc concentration}
+ \beta_2 \times \text{BOD}
+ \epsilon
\\

\Rightarrow \text{we estimated }\beta_1 = 0.08 (p=0.63), \beta_2 = -2.33(p=0.04)
$$

###### Then, $\beta_1$ became **close to zero**  and **the effect of "zinc concentration" was no longer observed**.

###### From this, we can infer that the correlation between "zinc concentration" and "biodiversity" is **due to confounding** and **not caused by zinc itself**.

---

##### So, the way "to estimate causal effect in **Confounding**" is **Cut the indirect upstream connection** between X and Y. 

###### -  one way is **adding confounding factors to explanatory variables**.

#### In order to do that ...

###### 1. imagine and draw structure of relations (it's called '**causal diagram**')
###### 2. consider **what will be confaunding factor** of X and Y
###### 3. observe the candidates of confounding factor similar to X and Y.

![bg left:35% 100%](因果ダイアグラム_2.drawio.png)

 <!-- So causal effect is close to 0.0. -->

---

# So what I mean...

##### - When discussing causal relation from observational data, we should consider **confounding factors**.

##### - When estimating causal effects from regression coefficients in regression analysis, we should **check confounding factors** and **add them to the explanatory variables**.

##### - When discussing a causal relationship between two factors, we **should not look at only the two factors**!We should consider the **surrounding causal diagram**.

---

# By the way, causal diagram is alike with "system thinking", right??:satisfied:

![bg left:50% 100%](因果ダイアグラム_2.drawio.png)

---

<!-- _class: title -->

# Thank you for your listening!

### pls enjoy your profound and interesting analytics life.:satisfied:

#### Reference

- Multiple Regression Viewed from Causal Inference Perspective
  統計的因果推論の視点による重回帰分析, Mahabu Iwasaki
- 岩波データサイエンス vol.3 因果推論-実世界のデータから因果を読む.
- zincの画像候補
  - https://www.911metallurgist.com/blog/high-zinc-levels-are-poisoning-the-new-river
  - https://hungarytoday.hu/concentration-zinc-copper-aluminium-iron-szamos-river-pollution-romania/
- BOD の画像候補
  - https://www.youtube.com/watch?v=URvWDDHF8NY
